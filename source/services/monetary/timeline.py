import pytz
from datetime import datetime, timedelta
from source.libraries.database.query import Query
from source.entities.stock import Stock as StockEntity
from source.enumerators.period import Period as PeriodEnum
from source.models.timeline import Timeline as TimelineModel
from source.entities.timeline import Timeline as TimelineEntity

class Timeline:

    def get_datetime_now(self, stock: StockEntity) -> datetime:
        result = datetime.now(pytz.timezone(stock.timezone))
        if result.hour < 16:
            result -= timedelta(days=1)
        while result.weekday() == 5 or result.weekday() == 6:
            result -= timedelta(days=1)
        return result.replace(hour=16, minute=0, second=0, microsecond=0)

    def get_timeline(self, stock: StockEntity, type: PeriodEnum, moment: datetime) -> TimelineEntity:
        if type == PeriodEnum.DAY:
            return self._get_timeline_day(stock, moment)
        raise Exception('Period not implemented')

    # momento fixado com 16 horas para tipo diario
    def _get_timeline_day(self, stock: StockEntity, moment: datetime) -> TimelineEntity:
        at = datetime.now(pytz.timezone(stock.timezone))
        at = at.replace(hour=16, minute=0, second=0, microsecond=0)
        at = at.replace(year=moment.year, month=moment.month, day=moment.day)
        query = Query()
        query.limit(1)
        query.select()
        query.table('timelines')
        query.order('datetime ASC')
        query.where(f"datetime = {query.quote(at)}")
        query.where(f"stock_id = {query.quote(stock.id)}")
        query.where(f"type = {query.quote(PeriodEnum.DAY)}")
        for model in TimelineModel.objects.raw(query.assemble()):
            return TimelineEntity(model)
        if at.weekday() == 5 and at.weekday() == 6:
            return None
        entity = TimelineEntity()
        entity.type = PeriodEnum.DAY
        entity.stock = stock
        entity.datetime = at
        entity.save()
        return entity