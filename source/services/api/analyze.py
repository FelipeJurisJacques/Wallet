from datetime import datetime
from source.libraries.database.fetch import Fetch
from source.libraries.database.query import Query
from source.enumerators.period import Period as PeriodEnumerator

class Analyze:
    def __init__(self):
        self.fetch = Fetch()
        self.query = Query()

    def get_all(self):
        return self.fetch.all(self.query.analyze.get_all())

    def get(self, id):
        return self.fetch.first(self.query.analyze.get(id))

    def get_all_from_stock(self, stock: int):
        self.query.select([
            'analyzes.id',
            'analyzes.period',
            'MAX(historical_timelines.datetime) AS historic_end_at',
            'MIN(historical_timelines.datetime) AS historic_start_at',
            'MAX(prophesied_timelines.datetime) AS prophesied_end_at',
            'MIN(prophesied_timelines.datetime) AS prophesied_start_at',
        ])
        self.query.table('analyzes')
        self.query.group('analyzes.id')
        self.query.where(f'analyzes.stock_id = {Query.quote(stock)}')
        self.query.inner('prophesied', 'prophesied.analyze_id = analyzes.id')
        self.query.inner('analyzes_timelines', 'analyzes.id = analyzes_timelines.analyze_id')
        self.query.inner(
            'timelines AS prophesied_timelines',
            'prophesied.timeline_id = prophesied_timelines.id'
        )
        self.query.inner(
            'timelines AS historical_timelines',
            'analyzes_timelines.timeline_id = historical_timelines.id'
        )
        rows = self.fetch.all(self.query)
        results = []
        for row in rows:
            results.append({
                'id': row['id'],
                'period': PeriodEnumerator(row['period']),
                'historic_end_at': datetime.fromtimestamp(row['historic_end_at']),
                'historic_start_at': datetime.fromtimestamp(row['historic_start_at']),
                'prophesied_end_at': datetime.fromtimestamp(row['prophesied_end_at']),
                'prophesied_start_at': datetime.fromtimestamp(row['prophesied_start_at']),
            })
        return results