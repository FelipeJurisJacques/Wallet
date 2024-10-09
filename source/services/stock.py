from ..models.stock import StockModel
from ..entities.stock import StockEntity

class StockService:

    def all(self) -> list[StockModel]:
        result = []
        for entity in StockEntity.objects.all():
            result.append(StockModel(entity))
        return result

    def get_by_symbol(self, symbol:str) -> StockModel:
        entities = StockEntity.objects.filter(symbol=symbol)[:1]
        for entity in entities:
            return StockModel(entity)
        return None