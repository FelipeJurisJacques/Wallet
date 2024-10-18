import datetime
from django.db.models import Max
from ..models.stock import StockModel
from ..models.prophesied import ProphesiedModel
from ..entities.prophesied import ProphesiedEntity
from ..enumerators.prophesied import ProphesiedEnum

class ProphesyService:

    def get_all_from_stock(self, stock:StockModel) -> list[ProphesiedModel]:
        entities = ProphesiedEntity.objects.filter(stock_id=stock.id).order_by('date')
        list = []
        for entity in entities:
            list.append(ProphesiedModel(entity))
        return list

    def get_period_from_stock(self, stock:StockModel, limit:int, offset:int) -> list[ProphesiedModel]:
        entities = ProphesiedEntity.objects.filter(stock_id=stock.id)[offset:limit]
        list = []
        for entity in entities:
            list.append(ProphesiedModel(entity))
        return list

    def get_max_date_from_stock(self, stock:StockModel, type: ProphesiedEnum) -> datetime.datetime:
        row = ProphesiedEntity.objects.filter(stock_id=stock.id, type=type.value).aggregate(max_date=Max('date'))
        if row['max_date']:
            return datetime.datetime.fromtimestamp(row['max_date'])
        return None