from datetime import datetime
from source.libraries.database.query import Query
from source.entities.stock import Stock as StockEntity
from source.enumerators.period import Period as PeriodEnum
from source.models.timeline import Timeline as TimelineModel
from source.entities.timeline import Timeline as TimelineEntity

class Timeline:

    def get_timeline(self, stock: StockEntity, type: PeriodEnum, date: datetime) -> TimelineEntity:
        query = Query()
        query.limit(1)
        query.select()
        query.order('date ASC')
        query.table('timelines')
        query.where(f"date = {query.quote(date)}")
        query.where(f"type = {query.quote(type)}")
        query.where(f"stock_id = {query.quote(stock.id)}")
        for model in TimelineModel.objects.raw(query.assemble()):
            return TimelineEntity(model)
        entity = TimelineEntity()
        entity.date = date
        entity.type = type
        entity.stock = stock
        entity.save()
        return entity