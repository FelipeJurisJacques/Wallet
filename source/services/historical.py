import datetime
from django.db.models import Max
from ..models.stock import StockModel
from ..models.historic_day import HistoricDayModel
from ..entities.historic_day import HistoricDayEntity

class HistoricalService:

    def get_all_from_stock(self, stock:StockModel) -> list[HistoricDayEntity]:
        entities = HistoricDayModel.objects.filter(stock_id=stock.id).order_by('date')
        list = []
        for entity in entities:
            list.append(HistoricDayEntity(entity))
        return list

    def get_period_from_stock(self, stock:StockModel, limit:int, offset:int) -> list[HistoricDayEntity]:
        entities = HistoricDayModel.objects.filter(stock_id=stock.id)[offset:limit]
        list = []
        for entity in entities:
            list.append(HistoricDayEntity(entity))
        return list
    
    def get_from_stock_date(self, stock:StockModel, date: datetime.datetime) -> HistoricDayEntity:
        result = HistoricDayModel.objects.filter(stock_id=stock.id, date=date.timestamp()).order_by('-date')[:1]
        if result.exists():
            return HistoricDayEntity(result[0])
        else:
            return None
    
    def get_last_date_from_stock(self, stock:StockModel) -> HistoricDayEntity:
        result = HistoricDayModel.objects.filter(stock_id=stock.id).order_by('-date')[:1]
        if result.exists():
            return HistoricDayEntity(result[0])
        else:
            return None

    def get_max_date_from_stock(self, stock:StockModel) -> datetime.date:
        row = HistoricDayModel.objects.filter(stock_id=stock.id).aggregate(max_date=Max('date'))
        if row['max_date']:
            return datetime.date.fromtimestamp(row['max_date'])
        return datetime.date.today() - datetime.timedelta(days=5*365)