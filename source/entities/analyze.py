from .entity import Entity
from ..entities.stock import Stock
from ..entities.historic import Historic
from ..models.analyze import Analyze as AnalyzeModel
from ..enumerators.period import Period as PeriodEnum

class Analyze(Entity):

    @staticmethod
    def find(id:int):
        result = AnalyzeModel.objects.filter(pk=id)
        if result.exists():
            return Analyze(result[0])
        else:
            return None

    def __init__(self, model: AnalyzeModel = None):
        self._historical = None
        if model is None:
            self._model = AnalyzeModel()
        else:
            self._model = model

    @property
    def id(self) -> int:
        return self._model.id

    @property
    def period(self) -> Stock:
        return PeriodEnum(self._model.period)

    @period.setter
    def period(self, value: PeriodEnum):
        self._model.period = value.value

    @property
    def historical(self) -> list[Historic]:
        if self._historical is None:
            entities = []
            for model in self._model.historical.all():
                entities.append(Stock(model))
            return entities
        return self._historical

    @historical.setter
    def historical(self, value: list[Historic]):
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
