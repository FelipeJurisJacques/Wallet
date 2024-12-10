import datetime
from .entity import Entity
from .period import PeriodEntity
from ..models.forecast import ForecastModel
from ..enumerators.historic import HistoricEnum

class ForecastEntity(Entity):

    @staticmethod
    def find(id:int):
        result = ForecastModel.objects.filter(pk=id)
        if result.exists():
            return ForecastEntity(result[0])
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
    def forecast_min_moment(self) -> datetime.datetime:
        if self._model.forecast_min_moment is None:
            return None
        else:
            return datetime.datetime.fromtimestamp(self._model.forecast_min_moment)

    @forecast_min_moment.setter
    def forecast_min_moment(self, value: datetime.datetime):
        self._model.forecast_min_moment = value.timestamp()

    @property
    def forecast_max_moment(self) -> datetime.datetime:
        if self._model.forecast_max_moment is None:
            return None
        else:
            return datetime.datetime.fromtimestamp(self._model.forecast_max_moment)

    @forecast_max_moment.setter
    def forecast_max_moment(self, value: datetime.datetime):
        self._model.forecast_max_moment = value.timestamp()

    @property
    def corrected_min_moment(self) -> datetime.datetime:
        if self._model.corrected_min_moment is None:
            return None
        else:
            return datetime.datetime.fromtimestamp(self._model.corrected_min_moment)

    @corrected_min_moment.setter
    def corrected_min_moment(self, value: datetime.datetime):
        self._model.corrected_min_moment = value.timestamp()

    @property
    def corrected_max_moment(self) -> datetime.datetime:
        if self._model.corrected_max_moment is None:
            return None
        else:
            return datetime.datetime.fromtimestamp(self._model.corrected_max_moment)

    @corrected_max_moment.setter
    def corrected_max_moment(self, value: datetime.datetime):
        self._model.corrected_max_moment = value.timestamp()

    @property
    def forecast_min_value(self) -> float:
        return float(self._model.forecast_min_value)

    @forecast_min_value.setter
    def forecast_min_value(self, value: float):
        self._model.forecast_min_value = value

    @property
    def forecast_max_value(self) -> float:
        return float(self._model.forecast_max_value)

    @forecast_max_value.setter
    def forecast_max_value(self, value: float):
        self._model.forecast_max_value = value

    @property
    def forecast_difference(self) -> float:
        return float(self._model.forecast_difference)

    @forecast_difference.setter
    def forecast_difference(self, value: float):
        self._model.forecast_difference = value

    @property
    def forecast_percentage(self) -> float:
        return float(self._model.forecast_percentage)

    @forecast_percentage.setter
    def forecast_percentage(self, value: float):
        self._model.forecast_percentage = value

    @property
    def corrected_min_value(self) -> float:
        if self._model.corrected_min_value is None:
            return None
        else:
            return float(self._model.corrected_min_value)

    @corrected_min_value.setter
    def corrected_min_value(self, value: float):
        self._model.corrected_min_value = value

    @property
    def corrected_max_value(self) -> float:
        if self._model.corrected_max_value is None:
            return None
        else:
            return float(self._model.corrected_max_value)

    @corrected_max_value.setter
    def corrected_max_value(self, value: float):
        self._model.corrected_max_value = value

    @property
    def corrected_difference(self) -> float:
        if self._model.corrected_difference is None:
            return None
        else:
            return float(self._model.corrected_difference)

    @corrected_difference.setter
    def corrected_difference(self, value: float):
        self._model.corrected_difference = value

    @property
    def corrected_percentage(self) -> float:
        if self._model.corrected_percentage is None:
            return None
        else:
            return float(self._model.corrected_percentage)

    @corrected_percentage.setter
    def corrected_percentage(self, value: float):
        self._model.corrected_percentage = value