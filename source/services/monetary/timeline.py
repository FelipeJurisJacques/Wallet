import pytz
from datetime import datetime, timedelta
from source.libraries.database.query import Query
from source.entities.stock import Stock as StockEntity
from source.enumerators.period import Period as PeriodEnum
from source.models.timeline import Timeline as TimelineModel
from source.entities.timeline import Timeline as TimelineEntity

class Timeline:

    def get_datetime_now(self, stock: StockEntity) -> datetime:
        date = datetime.now(pytz.timezone(stock.timezone))
        utc = 16
        if stock.timezone == 'EST':
            utc = 21
        if date.hour < utc:
            date -= timedelta(days=1)
        while date.weekday() == 5 or date.weekday() == 6:
            date -= timedelta(days=1)
        date.replace(hour=utc, minute=0, second=0, microsecond=0)
        return date

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
        date = date.astimezone(pytz.utc)
        moment = datetime.now(pytz.utc)
        if date.date() == moment.date():
            utc = 16
            if stock.timezone == 'EST':
                utc = 21
            if date.hour < utc:
                return None
        elif date.weekday() == 5 and moment.weekday() == 6:
            return None
        entity = TimelineEntity()
        entity.date = date
        entity.type = type
        entity.stock = stock
        entity.save()
        return entity