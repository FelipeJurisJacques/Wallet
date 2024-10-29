import datetime
from .entity import Entity
from .historic_day import HistoricDayEntity
from ..models.forecast_day import ForecastDayModel
from ..enumerators.quantitative import QuantitativeEnum

class ForecastDayEntity(Entity):

    @staticmethod
    def find(id:int):
        result = ForecastDayModel.objects.filter(pk=id)
        if result.exists():
            return ForecastDayEntity(result[0])
        else:
            return None

    def __init__(self, model: ForecastDayModel = None):
        if model is None:
            self._model = ForecastDayModel()
        else:
            self._model = model

    @property
    def id(self) -> int:
        return self._model.id

    @property
    def origin(self) -> QuantitativeEnum:
        return QuantitativeEnum(self._model.origin)

    @origin.setter
    def origin(self, value: QuantitativeEnum):
        self._model.origin = value.value

    @property
    def nested_historic(self) -> HistoricDayEntity:
        return HistoricDayEntity(self._model.nested_historic)

    @nested_historic.setter
    def nested_historic(self, value: HistoricDayEntity):
        self._model.nested_historic = value._model

    @property
    def consecutive_historic(self) -> HistoricDayEntity:
        return HistoricDayEntity(self._model.consecutive_historic)

    @consecutive_historic.setter
    def consecutive_historic(self, value: HistoricDayEntity):
        self._model.consecutive_historic = value._model
    
    @property
    def open_forecast_difference(self) -> float:
        return self._model.open_forecast_difference

    @open_forecast_difference.setter
    def open_forecast_difference(self, value: float):
        self._model.open_forecast_difference = value

    @property
    def open_forecast_percentage(self) -> float:
        return self._model.open_forecast_percentage

    @open_forecast_percentage.setter
    def open_forecast_percentage(self, value: float):
        self._model.open_forecast_percentage = value

    @property
    def close_forecast_difference(self) -> float:
        return self._model.close_forecast_difference

    @close_forecast_difference.setter
    def close_forecast_difference(self, value: float):
        self._model.close_forecast_difference = value

    @property
    def close_forecast_percentage(self) -> float:
        return self._model.close_forecast_percentage

    @close_forecast_percentage.setter
    def close_forecast_percentage(self, value: float):
        self._model.close_forecast_percentage = value

    @property
    def open_corrected_difference(self) -> float:
        return self._model.open_corrected_difference

    @open_corrected_difference.setter
    def open_corrected_difference(self, value: float):
        self._model.open_corrected_difference = value

    @property
    def open_corrected_percentage(self) -> float:
        return self._model.open_corrected_percentage

    @open_corrected_percentage.setter
    def open_corrected_percentage(self, value: float):
        self._model.open_corrected_percentage = value

    @property
    def close_corrected_difference(self) -> float:
        return self._model.close_corrected_difference

    @close_corrected_difference.setter
    def close_corrected_difference(self, value: float):
        self._model.close_corrected_difference = value

    @property
    def close_corrected_percentage(self) -> float:
        return self._model.close_corrected_percentage

    @close_corrected_percentage.setter
    def close_corrected_percentage(self, value: float):
        self._model.close_corrected_percentage = value

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