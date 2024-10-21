import datetime
from .entity import Entity
from ..models.historic_day import HistoricDayModel

class HistoricDayEntity(Entity):

    @staticmethod
    def find(id:int):
        result = HistoricDayModel.objects.filter(pk=id)
        if result.exists():
            return HistoricDayEntity(result[0])
        else:
            return None

    def __init__(self, model: HistoricDayModel = None):
        if model is None:
            self._model = HistoricDayModel()
        else:
            self._model = model

    @property
    def id(self) -> int:
        return self._model.id

    @property
    def low(self) -> float:
        return self._model.low

    @low.setter
    def low(self, value: float):
        self._model.low = value

    @property
    def date(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self._model.date)

    @date.setter
    def date(self, value: datetime.datetime):
        self._model.date = value.timestamp()

    @property
    def high(self) -> float:
        return self._model.high

    @high.setter
    def high(self, value: float):
        self._model.high = value

    @property
    def open(self) -> float:
        return self._model.open

    @open.setter
    def open(self, value: float):
        self._model.open = value

    @property
    def close(self) -> float:
        return self._model.close

    @close.setter
    def close(self, value: float):
        self._model.close = value

    @property
    def volume(self) -> float:
        return self._model.volume

    @volume.setter
    def volume(self, value: float):
        self._model.volume = value

    @property
    def stock_id(self) -> int:
        return self._model.stock_id

    @stock_id.setter
    def stock_id(self, value: int):
        self._model.stock_id = value

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