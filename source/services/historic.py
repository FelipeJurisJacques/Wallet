from datetime import datetime, timedelta
from ..libraries.database.fetch import Fetch
from ..libraries.database.query import Query
from ..entities.stock import Stock as StockEntity
from ..enumerators.period import Period as PeriodEnum
from ..models.historic import Historic as HistoricModel
from ..entities.timeline import Timeline as TimelineEntity
from ..entities.historic import Historic as HistoricEntity

class Historic:

    def get_max_historical_date(self, stock: StockEntity, type: PeriodEnum) -> datetime:
        fetch = Fetch()
        query = Query()
        query.limit(1)
        query.table('timelines')
        query.select('timelines.date')
        query.order('timelines.date DESC')
        query.where(f"timelines.type = {query.quote(type)}")
        query.where(f"timelines.stock_id = {query.quote(stock.id)}")
        query.inner('historical', 'historical.timeline_id = timelines.id')
        value = fetch.one(query)
        if value is not None:
            return datetime.fromtimestamp(value)
        else:
            return datetime.now() - timedelta(days=5*365)
    
    def get_historic(self, timeline: TimelineEntity) -> HistoricEntity:
        result = HistoricModel.objects.filter(timeline_id=timeline.id)[:1]
        if result.exists():
            return HistoricEntity(result[0])
        else:
            return None

    def get_all_from_stock(self, stock:StockEntity) -> list[HistoricEntity]:
        entities = HistoricModel.objects.filter(stock_id=stock.id).order_by('date')
        list = []
        for entity in entities:
            list.append(HistoricEntity(entity))
        return list

    def get_period_from_stock(self, stock:StockEntity, limit:int, offset:int) -> list[HistoricEntity]:
        entities = HistoricModel.objects.filter(stock_id=stock.id)[offset:limit]
        list = []
        for entity in entities:
            list.append(HistoricEntity(entity))
        return list
    
    def get_from_stock_date(self, stock:StockEntity, date: datetime) -> HistoricEntity:
        result = HistoricModel.objects.filter(stock_id=stock.id, date=date.timestamp()).order_by('-date')[:1]
        if result.exists():
            return HistoricEntity(result[0])
        else:
            return None
    
    def get_last_date_from_stock(self, stock:StockEntity) -> HistoricEntity:
        result = HistoricModel.objects.filter(stock_id=stock.id).order_by('-date')[:1]
        if result.exists():
            return HistoricEntity(result[0])
        else:
            return None