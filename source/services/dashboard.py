from datetime import datetime
from ..enumerators.period import PeriodEnum
from ..libraries.database.query import QueryLib
from ..libraries.database.fetch import FetchLib

class DashboardService:

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