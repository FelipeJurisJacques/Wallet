import datetime
from django.db.models import Max
from ..models.stock import StockModel
from ..models.prophesy_day import ProphesyDayModel
from ..models.historic_day import HistoricDayModel
from ..entities.prophesy_day import ProphesyDayEntity

class ProphesyService:

    def get_all_from_stock(self, stock:StockModel) -> list[ProphesyDayEntity]:
        entities = ProphesyDayModel.objects.filter(stock_id=stock.id).order_by('date')
        list = []
        for entity in entities:
            list.append(ProphesyDayEntity(entity))
        return list

    def get_period_from_stock(self, stock:StockModel, limit:int, offset:int) -> list[ProphesyDayEntity]:
        entities = ProphesyDayModel.objects.filter(stock_id=stock.id)[offset:limit]
        list = []
        for entity in entities:
            list.append(ProphesyDayEntity(entity))
        return list

    def get_max_date_from_stock(self, stock:StockModel) -> datetime.datetime:
        date = HistoricDayModel.objects.filter(
            stock_id=stock.id
        ).select_related(
            'prophesied_day'
        ).order_by(
            '-prophesied_day__last_historic_id'
        ).values_list(
            'date', flat=True
        ).first()
        if date in None:
            return None
        return datetime.datetime.fromtimestamp(date)