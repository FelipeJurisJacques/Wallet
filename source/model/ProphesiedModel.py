import datetime
from ..entities.ProphesiedEntity import ProphesiedEntity

class ProphesiedEntity:
    def __init__(self, historic: ProphesiedEntity):
        self._entity = historic

    @property
    def id(self) -> int:
        return self._entity.id

    @id.setter
    def id(self, value: int):
        self._entity.id = value

    @property
    def stockId(self) -> int:
        return self._entity.stock_id

    @stockId.setter
    def stockId(self, value: int):
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
    def yhatLower(self) -> float:
        return self._entity.yhat_lower

    @yhatLower.setter
    def yhatLower(self, value: float):
        self._entity.yhat_lower = value

    @property
    def yhatUpper(self) -> float:
        return self._entity.yhat_upper

    @yhatUpper.setter
    def yhatUpper(self, value: float):
        self._entity.yhat_upper = value

    @property
    def trendLower(self) -> float:
        return self._entity.trend_lower

    @trendLower.setter
    def trendLower(self, value: float):
        self._entity.trend_lower = value

    @property
    def trendUpper(self) -> float:
        return self._entity.trend_upper

    @trendUpper.setter
    def trendUpper(self, value: float):
        self._entity.trend_upper = value

    @property
    def additiveTerms(self) -> float:
        return self._entity.additive_terms

    @additiveTerms.setter
    def additive_terms(self, value: float):
        self._entity.additive_terms = value

    @property
    def additiveTermsLower(self) -> float:
        return self._entity.additive_terms_lower

    @additiveTermsLower.setter
    def additive_terms_lower(self, value: float):
        self._entity.additive_terms_lower = value

    @property
    def additiveTermsUpper(self) -> float:
        return self._entity.additive_terms_upper

    @additiveTermsUpper.setter
    def additive_terms_upper(self, value: float):
        self._entity.additive_terms_upper = value

    @property
    def weekly(self) -> float:
        return self._entity.weekly

    @weekly.setter
    def weekly(self, value: float):
        self._entity.weekly = value

    @property
    def weeklyLower(self) -> float:
        return self._entity.weekly_lower

    @weeklyLower.setter
    def weeklyLower(self, value: float):
        self._entity.weekly_lower = value

    @property
    def weeklyUpper(self) -> float:
        return self._entity.weekly_upper

    @weeklyUpper.setter
    def weeklyUpper(self, value: float):
        self._entity.weekly_upper = value

    @property
    def multiplicativeTerms(self) -> float:
        return self._entity.multiplicative_terms

    @multiplicativeTerms.setter
    def multiplicativeTerms(self, value: float):
        self._entity.multiplicative_terms = value

    @property
    def multiplicativeTermsLower(self) -> float:
        return self._entity.multiplicative_terms_lower

    @multiplicativeTermsLower.setter
    def multiplicative_terms_lower(self, value: float):
        self._entity.multiplicative_terms_lower = value

    @property
    def multiplicativeTermsUpper(self) -> float:
        return self._entity.multiplicative_terms_upper

    @multiplicativeTermsUpper.setter
    def multiplicative_terms_upper(self, value: float):
        self._entity.multiplicative_terms_upper = value

    @property
    def yhat(self) -> float:
        return self._entity.yhat

    @yhat.setter
    def yhat(self, value: float):
        self._entity.yhat = value