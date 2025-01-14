import datetime
from .entity import Entity
from .period import Period as PeriodEntity
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
    def period(self) -> PeriodEntity:
        return PeriodEntity(self._model.period)

    @period.setter
    def period(self, value: PeriodEntity):
        self._model.period = value._model

    @property
    def min_date(self) -> datetime.datetime:
        if self._model.min_date is None:
            return None
        else:
            return datetime.datetime.fromtimestamp(self._model.min_date)

    @min_date.setter
    def min_date(self, value: datetime.datetime):
        self._model.min_date = value.timestamp()

    @property
    def max_date(self) -> datetime.datetime:
        if self._model.max_date is None:
            return None
        else:
            return datetime.datetime.fromtimestamp(self._model.max_date)

    @max_date.setter
    def max_date(self, value: datetime.datetime):
        self._model.max_date = value.timestamp()

    @property
    def interval(self) -> int:
        if self._model.interval is None:
            return None
        else:
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