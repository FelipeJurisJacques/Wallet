from .entity import Entity
from ..models.period import PeriodModel
from ..entities.stock import StockEntity
from ..enumerators.period import PeriodEnum
from ..entities.historic import HistoricEntity

class PeriodEntity(Entity):

    @staticmethod
    def find(id:int):
        result = PeriodModel.objects.filter(pk=id)
        if result.exists():
            return PeriodEntity(result[0])
        else:
            return None

    def __init__(self, model: PeriodModel = None):
        if model is None:
            self._model = PeriodModel()
        else:
            self._model = model

    @property
    def id(self) -> int:
        return self._model.id

    @property
    def period(self) -> StockEntity:
        return PeriodEnum(self._model.period)

    @period.setter
    def period(self, value: PeriodEnum):
        self._model.period = value.value

    @property
    def historical(self) -> list[HistoricEntity]:
        entities = []
        for model in self._model.historical:
            entities.append(StockEntity(model))
        return entities

    @historical.setter
    def historical(self, value: list[HistoricEntity]):
        models = []
        for entity in value:
            models.append(entity._model)
        self._model.historical = models
