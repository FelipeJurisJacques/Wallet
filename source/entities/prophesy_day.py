import datetime
from .entity import Entity
from ..entities.stock import StockEntity
from ..models.prophesy_day import ProphesyDayModel
from ..enumerators.prophesied import ProphesiedEnum
from ..entities.historic_day import HistoricDayEntity

class ProphesyDayEntity(Entity):

    @staticmethod
    def find(id:int):
        result = ProphesyDayModel.objects.filter(pk=id)
        if result.exists():
            return ProphesyDayEntity(result[0])
        else:
            return None

    def __init__(self, model: ProphesyDayModel = None):
        if model is None:
            self._model = ProphesyDayModel()
        else:
            self._model = model

    @property
    def id(self) -> int:
        return self._model.id

    @property
    def type(self) -> ProphesiedEnum:
        return ProphesiedEnum(self._model.type)

    @type.setter
    def type(self, value: ProphesiedEnum):
        self._model.type = value.value

    @property
    def stock(self) -> StockEntity:
        return StockEntity(self._model.stock_id)

    @stock.setter
    def stock(self, value: StockEntity):
        self._model.stock_id = value._model

    @property
    def stock_id(self) -> int:
        return self._model.stock_id.id

    @property
    def increased_day(self) -> int:
        return self._model.increased_day

    @increased_day.setter
    def increased_day(self, value: int):
        self._model.increased_day = value

    @property
    def last_historic(self) -> HistoricDayEntity:
        return HistoricDayEntity(self._model.last_historic_id)

    @stock.setter
    def last_historic(self, value: HistoricDayEntity):
        self._model.last_historic_id = value._model

    @property
    def last_historic_id(self) -> int:
        return self._model.last_historic_id.id

    @property
    def data_start_date(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self._model.data_start_date)

    @data_start_date.setter
    def data_start_date(self, value: datetime.datetime):
        self._model.data_start_date = value.timestamp()

    @property
    def data_end_date(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self._model.data_end_date)

    @data_end_date.setter
    def data_end_date(self, value: datetime.datetime):
        self._model.data_end_date = value.timestamp()

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

    @property
    def created(self) -> datetime.datetime:
        if not self._model.created:
            return None
        else:
            return datetime.datetime.fromtimestamp(self._model.created)

    @property
    def updated(self) -> datetime.datetime:
        if not self._model.updated:
            return None
        else:
            return datetime.datetime.fromtimestamp(self._model.updated)

    def save(self):        
        if not self._model.created:
            self._model.created = datetime.datetime.now().timestamp()
        if not self._model.updated:
            self._model.updated = datetime.datetime.now().timestamp()
        super().save()
