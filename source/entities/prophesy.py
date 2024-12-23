import datetime
from .entity import Entity
from .period import PeriodEntity
from ..models.prophesy import ProphesyModel
from ..enumerators.historic import HistoricEnum

class ProphesyEntity(Entity):

    @staticmethod
    def find(id:int):
        result = ProphesyModel.objects.filter(pk=id)
        if result.exists():
            return ProphesyEntity(result[0])
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
    def period(self) -> PeriodEntity:
        return PeriodEntity(self._model.period)

    @period.setter
    def period(self, value: PeriodEntity):
        self._model.period = value._model

    @property
    def increased(self) -> int:
        return self._model.increased

    @increased.setter
    def increased(self, value: int):
        self._model.increased = value

    @property
    def date(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self._model.date)

    @date.setter
    def date(self, value: datetime.datetime):
        self._model.date = value.timestamp()

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