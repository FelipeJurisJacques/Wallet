from datetime import datetime
from ..enumerators.period import PeriodEnum
from ..libraries.database.query import QueryLib
from ..libraries.database.fetch import FetchLib
from ..enumerators.historic import HistoricEnum

class DashboardService:

    def get_historical(self, stock: int, start_date: datetime, end_date: datetime) -> list[dict]:
        fetch = FetchLib()
        query = QueryLib()
        query.table('historical')
        query.order('date ASC')
        query.select([
            'date',
            'close',
        ])
        query.where(f"stock_id = {Query.quote(stock)}")
        query.where(f"type = {Query.quote(PeriodEnum.DAY)}")
        query.where(f"date <= {Query.quote(end_date.timestamp())}")
        query.where(f"date >= {Query.quote(start_date.timestamp())}")
        rows = fetch.all(query)
        if len(rows) == 0:
            return []
        results = []
        for row in rows:
            results.append({
                'date': datetime.fromtimestamp(row.get('date')),
                'close': row.get('close'),
            })
        return results

    def get_period_prophesied(self, period: int) -> list[dict]:
        fetch = FetchLib()
        query = QueryLib()
        query.table('prophesied')
        query.order('date ASC')
        query.select([
            'date',
            'yhat',
        ])
        query.where(f"period_id = {Query.quote(period)}")
        query.where(f"type = {Query.quote(HistoricEnum.CLOSE)}")
        rows = fetch.all(query)
        if len(rows) == 0:
            return []
        results = []
        for row in rows:
            results.append({
                'date': datetime.fromtimestamp(row.get('date')),
                'close': row.get('yhat'),
            })
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
        query.where(f"historical.stock_id = {Query.quote(stock)}")
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