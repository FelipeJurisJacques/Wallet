from .entity import Entity
from .analyze import Analyze
from .timeline import Timeline
from ..models.forecast import Forecast as ForecastModel
from ..enumerators.historic import Historic as HistoricEnum

class Forecast(Entity):

    @staticmethod
    def find(id:int):
        result = ForecastModel.objects.filter(pk=id)
        if result.exists():
            return Forecast(result[0])
        else:
            return None

    def __init__(self, model: ForecastModel = None):
        if model is None:
            self._model = ForecastModel()
        else:
            self._model = model

    @property
    def id(self) -> int:
        return self._model.id

    @property
    def type(self) -> HistoricEnum:
        return HistoricEnum(self._model.type)

    @type.setter
    def type(self, value: HistoricEnum):
        self._model.type = value.value

    @property
    def analyze(self) -> Analyze:
        return Analyze(self._model.analyze)
    
    @analyze.setter
    def analyze(self, value: Analyze):
        self._model.analyze = value._model

    @property
    def min_timeline(self) -> Timeline:
        return Timeline(self._model.min_timeline)

    @min_timeline.setter
    def min_timeline(self, value: Timeline):
        self._model.min_timeline = value._model

    @property
    def max_timeline(self) -> Timeline:
        return Timeline(self._model.max_timeline)

    @max_timeline.setter
    def max_timeline(self, value: Timeline):
        self._model.max_timeline = value._model

    @property
    def interval(self) -> int:
        return self._model.interval

    @interval.setter
    def interval(self, value: int):
        self._model.interval = value

    @property
    def min_value(self) -> float:
        return float(self._model.min_value)

    @min_value.setter
    def min_value(self, value: float):
        self._model.min_value = value

    @property
    def max_value(self) -> float:
        return float(self._model.max_value)

    @max_value.setter
    def max_value(self, value: float):
        self._model.max_value = value

    @property
    def difference(self) -> float:
        return float(self._model.difference)

    @difference.setter
    def difference(self, value: float):
        self._model.difference = value

    @property
    def percentage(self) -> float:
        return float(self._model.percentage)

    @percentage.setter
    def percentage(self, value: float):
        self._model.percentage = value

    @property
    def quantitative(self) -> float:
        return self._model.quantitative

    @quantitative.setter
    def quantitative(self, value: float):
        self._model.quantitative = value