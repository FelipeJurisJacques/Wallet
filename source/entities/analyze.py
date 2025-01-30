from .entity import Entity
from .timeline import Timeline
from ..entities.stock import Stock
from ..models.analyze import Analyze as AnalyzeModel
from ..enumerators.period import Period as PeriodEnum
from ..enumerators.context import Context as ContextEnum

class Analyze(Entity):

    @staticmethod
    def find(id:int):
        result = AnalyzeModel.objects.filter(pk=id)
        if result.exists():
            return Analyze(result[0])
        else:
            return None

    def __init__(self, model: AnalyzeModel = None):
        self._timelines = None
        if model is None:
            self._model = AnalyzeModel()
        else:
            self._model = model

    @property
    def id(self) -> int:
        return self._model.id

    @property
    def stock(self) -> Stock:
        return Stock(self._model.stock)

    @stock.setter
    def stock(self, value: Stock):
        self._model.stock = value._model

    @property
    def period(self) -> Stock:
        return PeriodEnum(self._model.period)

    @period.setter
    def period(self, value: PeriodEnum):
        self._model.period = value.value

    @property
    def context(self) -> ContextEnum:
        return ContextEnum(self._model.context)

    @context.setter
    def context(self, value: ContextEnum):
        self._model.context = value.value

    @property
    def timelines(self) -> list[Timeline]:
        if self._timelines is None:
            entities = []
            for model in self._model.timelines.all():
                entities.append(Timeline(model))
            return entities
        return self._timelines

    @timelines.setter
    def timelines(self, value: list[Timeline]):
        self._timelines = value

    def save(self):
        super().save()
        if self._timelines is not None:
            models = []
            for entity in self._timelines:
                models.append(entity._model)
            if len(self._timelines) == 0:
                self._model.timelines.clear()
            else:
                self._model.timelines.set(models)
