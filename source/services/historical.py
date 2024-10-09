import datetime
from django.db.models import Max
from ..models.stock import StockModel
from ..models.historic import HistoricModel
from ..entities.historic import HistoricEntity

class HistoricalService:

    def get_all_from_stock(self, stock:StockModel) -> list[HistoricModel]:
        entities = HistoricEntity.objects.filter(stock_id=stock.id)
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

    def get_max_date(self, stock:StockModel) -> datetime.date:
        row = HistoricEntity.objects.filter(stock_id=stock.id).aggregate(max_date=Max('date'))
        if row['max_date']:
            return datetime.date.fromtimestamp(row['max_date'])
        return datetime.date.today() - datetime.timedelta(days=5*365)

    def add(self, stock:StockModel, date, open, high, low, close, volume):
        entity = HistoricEntity()
        entity.low = low
        entity.date = date.timestamp()
        entity.open = open
        entity.high = high
        entity.close = close
        entity.volume = volume
        entity.stock_id = stock.id
        entity.save()