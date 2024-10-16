import datetime
from django.db.models import Max
from ..models.stock import StockModel
from ..models.historic import HistoricModel
from ..entities.historic import HistoricEntity

class HistoricalService:

    def get_all_from_stock(self, stock:StockModel) -> list[HistoricModel]:
        entities = HistoricEntity.objects.filter(stock_id=stock.id).order_by('date')
        list = []
        for entity in entities:
            list.append(HistoricModel(entity))
        return list

    def get_period_from_stock(self, stock:StockModel, limit:int, offset:int) -> list[HistoricModel]:
        entities = HistoricEntity.objects.filter(stock_id=stock.id)[offset:limit]
        list = []
        for entity in entities:
            list.append(HistoricModel(entity))
        return list
    
    def get_from_stock_date(self, stock:StockModel, date: datetime.datetime) -> HistoricModel:
        result = HistoricEntity.objects.filter(stock_id=stock.id, date=date.timestamp()).order_by('-date')[:1]
        if result.exists():
            return HistoricModel(result[0])
        else:
            return None
    
    def get_last_date_from_stock(self, stock:StockModel) -> HistoricModel:
        result = HistoricEntity.objects.filter(stock_id=stock.id).order_by('-date')[:1]
        if result.exists():
            return HistoricModel(result[0])
        else:
            return None

    def get_max_date_from_stock(self, stock:StockModel) -> datetime.date:
        row = HistoricEntity.objects.filter(stock_id=stock.id).aggregate(max_date=Max('date'))
        if row['max_date']:
            return datetime.date.fromtimestamp(row['max_date'])
        return datetime.date.today() - datetime.timedelta(days=5*365)