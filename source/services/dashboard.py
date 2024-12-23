from datetime import datetime
from ..enumerators.period import PeriodEnum
from ..libraries.database.query import QueryLib
from ..libraries.database.fetch import FetchLib
from ..enumerators.historic import HistoricEnum

class DashboardService:

    def get_period_prophesied(self, period: int) -> list[dict]:
        fetch = FetchLib()
        query = QueryLib()
        query.table('prophesied')
        query.order('prophesied.date ASC')
        query.select([
            'prophesied.date',
            'prophesied.yhat',
            'historical.type',
            'historical.stock_id',
            'prophesied.increased',
        ])
        query.inner('periods', 'periods.id = prophesied.period_id')
        query.inner('periods_historical', 'periods_historical.periodmodel_id = periods.id') 
        query.inner('historical', 'historical.id = periods_historical.historicmodel_id')
        query.where(f"prophesied.period_id = {query.quote(period)}")
        query.where(f"prophesied.type = {query.quote(HistoricEnum.CLOSE)}")
        rows = fetch.all(query)
        if len(rows) == 0:
            return []
        type = None
        stock = None
        results = []
        for row in rows:
            if type is None or stock is None:
                type = row.get('type')
                stock = row.get('stock_id')
            results.append({
                'prophesy_date': datetime.fromtimestamp(row.get('date')),
                'prophesy_close': row.get('yhat'),
                'prophesy_increased': row.get('increased'),
            })
        query = QueryLib()
        query.table('historical')
        query.select([
            'historical.date',
            'historical.close',
        ])
        query.where(f"historical.type = {query.quote(type)}")
        query.where(f"historical.stock_id = {query.quote(stock)}")
        query.where(f'historical.date >= {query.quote(rows[0].get('date'))}')
        query.where(f'historical.date <= {query.quote(rows[-1].get('date'))}')
        rows = fetch.all(query)
        i = 0
        for result in results:
            historical = rows[i]
            result['historic_close'] = historical.get('close')
            result['historic_date'] = datetime.fromtimestamp(historical.get('date'))
        return results

    def get_all_periods_from_stock(self, stock: int) -> list:
        fetch = FetchLib()
        query = QueryLib()
        query.table('periods')
        query.select([
            'periods.id',
            'periods.period',
            'historical.type',
            'MAX(prophesied.increased) AS increased',
            'MAX(prophesied.date) AS max_prophesied_date',
            'MIN(prophesied.date) AS min_prophesied_date',
        ])
        query.group('periods.id')
        query.inner('periods_historical', 'periods_historical.periodmodel_id = periods.id')
        query.inner('historical', 'historical.id = periods_historical.historicmodel_id')
        query.left('prophesied', 'prophesied.period_id = periods.id')
        query.where(f"historical.stock_id = {query.quote(stock)}")
        rows = fetch.all(query)
        results = []
        for row in rows:
            results.append({
                'id': row.get('id'),
                'type': PeriodEnum(row.get('type')),
                'period': PeriodEnum(row.get('period')),
                'increased': row.get('increased'),
                'max_prophesied_date': datetime.fromtimestamp(row.get('max_prophesied_date')),
                'min_prophesied_date': datetime.fromtimestamp(row.get('min_prophesied_date')),
            })
        return results