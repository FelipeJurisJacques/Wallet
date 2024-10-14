import datetime
from ..entities.Entity import Entity

class ProphesiedModel:
    def __init__(self, entity: Entity = None):
        if entity is None:
            self._entity = Entity()
        else:
            self._entity = entity

    @property
    def id(self) -> int:
        return self._entity.id

    @property
    def stock_id(self) -> int:
        return self._entity.stock_id

    @stock_id.setter
    def stock_id(self, value: int):
        self._entity.stock_id = value

    @property
    def date(self) -> datetime.date:
        return datetime.date.fromtimestamp(self._entity.date)

    @date.setter
    def date(self, value: datetime.date):
        self._entity.date = value.timestamp()

    @property
    def trend(self) -> float:
        return self._entity.trend

    @trend.setter
    def trend(self, value: float):
        self._entity.trend = value

    @property
    def yhat_lower(self) -> float:
        return self._entity.yhat_lower

    @yhat_lower.setter
    def yhat_lower(self, value: float):
        self._entity.yhat_lower = value

    @property
    def yhat_upper(self) -> float:
        return self._entity.yhat_upper

    @yhat_upper.setter
    def yhat_upper(self, value: float):
        self._entity.yhat_upper = value

    @property
    def trend_lower(self) -> float:
        return self._entity.trend_lower

    @trend_lower.setter
    def trend_lower(self, value: float):
        self._entity.trend_lower = value

    @property
    def trend_upper(self) -> float:
        return self._entity.trend_upper

    @trend_upper.setter
    def trend_upper(self, value: float):
        self._entity.trend_upper = value

    @property
    def additive_terms(self) -> float:
        return self._entity.additive_terms

    @additive_terms.setter
    def additive_terms(self, value: float):
        self._entity.additive_terms = value

    @property
    def additive_terms_lower(self) -> float:
        return self._entity.additive_terms_lower

    @additive_terms_lower.setter
    def additive_terms_lower(self, value: float):
        self._entity.additive_terms_lower = value

    @property
    def additive_terms_upper(self) -> float:
        return self._entity.additive_terms_upper

    @additive_terms_upper.setter
    def additive_terms_upper(self, value: float):
        self._entity.additive_terms_upper = value

    @property
    def weekly(self) -> float:
        return self._entity.weekly

    @weekly.setter
    def weekly(self, value: float):
        self._entity.weekly = value

    @property
    def weekly_lower(self) -> float:
        return self._entity.weekly_lower

    @weekly_lower.setter
    def weekly_lower(self, value: float):
        self._entity.weekly_lower = value

    @property
    def weekly_upper(self) -> float:
        return self._entity.weekly_upper

    @weekly_upper.setter
    def weekly_upper(self, value: float):
        self._entity.weekly_upper = value

    @property
    def multiplicative_terms(self) -> float:
        return self._entity.multiplicative_terms

    @multiplicative_terms.setter
    def multiplicative_terms(self, value: float):
        self._entity.multiplicative_terms = value

    @property
    def multiplicative_terms_lower(self) -> float:
        return self._entity.multiplicative_terms_lower

    @multiplicative_terms_lower.setter
    def multiplicative_terms_lower(self, value: float):
        self._entity.multiplicative_terms_lower = value

    @property
    def multiplicative_terms_upper(self) -> float:
        return self._entity.multiplicative_terms_upper

    @multiplicative_terms_upper.setter
    def multiplicative_terms_upper(self, value: float):
        self._entity.multiplicative_terms_upper = value

    @property
    def yhat(self) -> float:
        return self._entity.yhat

    @yhat.setter
    def yhat(self, value: float):
        self._entity.yhat = value

    @property
    def created(self) -> float:
        return self._entity.created

    @created.setter
    def created(self, value: float):
        self._entity.created = value

    @property
    def umpdated(self) -> float:
        return self._entity.umpdated

    @umpdated.setter
    def umpdated(self, value: float):
        self._entity.umpdated = value
