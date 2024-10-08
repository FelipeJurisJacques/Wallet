from ..models.stock import StockModel
from ..entities.stock import StockEntity

class StockService:

    def all(self) -> list[StockModel]:
        result = []
        for entity in StockEntity.objects.all():
            result.append(StockModel(entity))
        return result