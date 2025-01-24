from datetime import datetime
from source.libraries.database.fetch import Fetch
from source.libraries.database.query import Query
from source.enumerators.historic import Historic as HistoricEnumerator

class Timeline:
    def __init__(self):
        self.fetch = Fetch()
        self.query = Query()

    def get_all_from_analyze(self, analyze: int):
        self.query.select([
            'timelines.id',
            'timelines.datetime',
            'historical.close AS historic_close',
            'prophesied_close.yhat AS prophesy_close',
        ])
        self.query.table('timelines')
        self.query.order('timelines.datetime ASC')
        self.query.inner('historical', 'historical.timeline_id = timelines.id')
        self.query.where(f'prophesied_close.analyze_id = {Query.quote(analyze)}')
        self.query.inner('prophesied AS prophesied_close', Query.operator_and([
            'prophesied_close.timeline_id = timelines.id',
            f'prophesied_close.type = {Query.quote(HistoricEnumerator.CLOSE)}',
        ]))
        rows = self.fetch.all(self.query)
        results = []
        for row in rows:
            results.append({
                'id': row['id'],
                'historic_close': row['historic_close'],
                'prophesy_close': row['prophesy_close'],
                'at': datetime.fromtimestamp(row['datetime']),
            })
        return results