from .entity import Entity
from .analyze import Analyze
from .timeline import Timeline as TimelineEntity
from ..models.prophesy import Prophesy as ProphesyModel
from ..enumerators.historic import Historic as HistoricEnum

class Prophesy(Entity):

    @staticmethod
    def find(id:int):
        result = ProphesyModel.objects.filter(pk=id)
        if result.exists():
            return Prophesy(result[0])
        else:
            return None

    def __init__(self, model: ProphesyModel = None):
        if model is None:
            self._model = ProphesyModel()
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
    def timeline(self) -> TimelineEntity:
        return TimelineEntity(self._model.timeline)

    @timeline.setter
    def timeline(self, value: TimelineEntity):
        self._model.timeline = value._model

    @property
    def trend(self) -> float:
        return self._model.trend

    @trend.setter
    def trend(self, value: float):
        self._model.trend = value

    @property
    def yhat_lower(self) -> float:
        return self._model.yhat_lower

    @yhat_lower.setter
    def yhat_lower(self, value: float):
        self._model.yhat_lower = value

    @property
    def yhat_upper(self) -> float:
        return self._model.yhat_upper

    @yhat_upper.setter
    def yhat_upper(self, value: float):
        self._model.yhat_upper = value

    @property
    def trend_lower(self) -> float:
        return self._model.trend_lower

    @trend_lower.setter
    def trend_lower(self, value: float):
        self._model.trend_lower = value

    @property
    def trend_upper(self) -> float:
        return self._model.trend_upper

    @trend_upper.setter
    def trend_upper(self, value: float):
        self._model.trend_upper = value

    @property
    def additive_terms(self) -> float:
        return self._model.additive_terms

    @additive_terms.setter
    def additive_terms(self, value: float):
        self._model.additive_terms = value

    @property
    def additive_terms_lower(self) -> float:
        return self._model.additive_terms_lower

    @additive_terms_lower.setter
    def additive_terms_lower(self, value: float):
        self._model.additive_terms_lower = value

    @property
    def additive_terms_upper(self) -> float:
        return self._model.additive_terms_upper

    @additive_terms_upper.setter
    def additive_terms_upper(self, value: float):
        self._model.additive_terms_upper = value

    @property
    def weekly(self) -> float:
        return self._model.weekly

    @weekly.setter
    def weekly(self, value: float):
        self._model.weekly = value

    @property
    def weekly_lower(self) -> float:
        return self._model.weekly_lower

    @weekly_lower.setter
    def weekly_lower(self, value: float):
        self._model.weekly_lower = value

    @property
    def weekly_upper(self) -> float:
        return self._model.weekly_upper

    @weekly_upper.setter
    def weekly_upper(self, value: float):
        self._model.weekly_upper = value

    @property
    def multiplicative_terms(self) -> float:
        return self._model.multiplicative_terms

    @multiplicative_terms.setter
    def multiplicative_terms(self, value: float):
        self._model.multiplicative_terms = value

    @property
    def multiplicative_terms_lower(self) -> float:
        return self._model.multiplicative_terms_lower

    @multiplicative_terms_lower.setter
    def multiplicative_terms_lower(self, value: float):
        self._model.multiplicative_terms_lower = value

    @property
    def multiplicative_terms_upper(self) -> float:
        return self._model.multiplicative_terms_upper

    @multiplicative_terms_upper.setter
    def multiplicative_terms_upper(self, value: float):
        self._model.multiplicative_terms_upper = value

    @property
    def yhat(self) -> float:
        return self._model.yhat

    @yhat.setter
    def yhat(self, value: float):
        self._model.yhat = value