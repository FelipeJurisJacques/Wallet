from .entity import Entity
from ..models.period import Period as PeriodModel
from ..entities.stock import Stock as StockEntity
from ..enumerators.period import Period as PeriodEnum
from ..entities.historic import Historic as HistoricEntity

class Period(Entity):

    @staticmethod
    def find(id:int):
        result = PeriodModel.objects.filter(pk=id)
        if result.exists():
            return Period(result[0])
        else:
            return None

    def __init__(self, model: PeriodModel = None):
        self._historical = None
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
        if self._historical is None:
            entities = []
            for model in self._model.historical.all():
                entities.append(StockEntity(model))
            return entities
        return self._historical

    @historical.setter
    def historical(self, value: list[HistoricEntity]):
        self._historical = value

    def save(self):
        super().save()
        if self._historical is not None:
            models = []
            for entity in self._historical:
                models.append(entity._model)
            if len(self._historical) == 0:
                self._model.historical.clear()
            else:
                self._model.historical.set(models)
