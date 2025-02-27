import pytz
from datetime import datetime, timedelta
from source.libraries.database.fetch import Fetch
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

    def get_min_datetime(self, type: PeriodEnum) -> datetime:
        fetch = Fetch()
        query = Query()
        query.limit(1)
        query.select('datetime')
        query.table('timelines')
        query.order('datetime ASC')
        query.where(f"type = {Query.quote(type)}")
        value = fetch.one(query)
        if value is None:
            return None
        else:
            return datetime.fromtimestamp(value)

    def get_timeline(self, stock: StockEntity, type: PeriodEnum, moment: datetime) -> TimelineEntity:
        if type == PeriodEnum.DAY:
            return self._get_timeline_day(stock, moment)
        raise Exception('Period not implemented')

    def is_working(self, moment: datetime) -> bool:
        return moment.weekday() != 5 and moment.weekday() != 6

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
        query.where(f"datetime = {Query.quote(at)}")
        query.where(f"stock_id = {Query.quote(stock.id)}")
        query.where(f"type = {Query.quote(PeriodEnum.DAY)}")
        for model in TimelineModel.objects.raw(query.assemble()):
            return TimelineEntity(model)
        entity = TimelineEntity()
        entity.type = PeriodEnum.DAY
        entity.stock = stock
        entity.working = self.is_working(at)
        entity.datetime = at
        entity.save()
        return entity