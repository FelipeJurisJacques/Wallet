from datetime import datetime
from source.libraries.database.query import Query
from source.entities.stock import Stock as StockEntity
from source.models.historic import Historic as HistoricModel
from source.entities.historic import Historic as HistoricEntity

class Historic:

    def get_historical(self, stock: StockEntity, start: datetime, end: datetime) -> list[HistoricEntity]:
        query = Query()
        query.table('historical')
        query.select('historical.*')
        query.order('timelines.datetime')
        query.where(f'timelines.stock_id = {stock.id}')
        query.where(f'timelines.datetime <= {Query.quote(end)}')
        query.where(f'timelines.datetime >= {Query.quote(start)}')
        query.inner('timelines', 'timelines.id = historical.timeline_id')
        models = HistoricModel.objects.raw(query.assemble())
        entities = []
        for model in models:
            entities.append(HistoricEntity(model))
        return entities