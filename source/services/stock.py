from ..models.stock import StockModel
from ..entities.stock import StockEntity
from source.enumerators.api import ApiEnum

class StockService:

    def all(self) -> list[StockEntity]:
        result = []
        for entity in StockModel.objects.all():
            result.append(StockEntity(entity))
        return result

    def all_from_api(self, api: ApiEnum) -> list[StockEntity]:
        result = []
        for entity in StockModel.objects.filter(api=api.value):
            result.append(StockEntity(entity))
        return result

    def get_by_symbol(self, symbol:str) -> StockEntity:
        entities = StockModel.objects.filter(symbol=symbol)[:1]
        for entity in entities:
            return StockEntity(entity)
        return None