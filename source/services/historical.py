import datetime
from django.db.models import Max
from ..entities.stock import StockEntity
from ..models.historic import HistoricModel
from ..enumerators.period import PeriodEnum
from ..entities.historic import HistoricEntity

class HistoricalService:
    
    def get_historic(self, stock:StockEntity, period:PeriodEnum, date: datetime.datetime) -> HistoricEntity:
        result = HistoricModel.objects.filter(stock_id=stock.id, period=period, date=date.timestamp())[:1]
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
    
    def get_from_stock_date(self, stock:StockEntity, date: datetime.datetime) -> HistoricEntity:
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

    def get_max_date_from_stock(self, stock:StockEntity) -> datetime.date:
        row = HistoricModel.objects.filter(stock_id=stock.id).aggregate(max_date=Max('date'))
        if row['max_date']:
            return datetime.date.fromtimestamp(row['max_date'])
        return datetime.date.today() - datetime.timedelta(days=5*365)