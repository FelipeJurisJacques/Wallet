import datetime
from .model import Model
from ..entities.historic import HistoricEntity

class HistoricModel(Model):
    def __init__(self, entity: HistoricEntity = None):
        if entity is None:
            self._entity = HistoricEntity()
        else:
            self._entity = entity

    @property
    def id(self) -> int:
        return self._entity.id

    @property
    def low(self) -> float:
        return self._entity.low

    @low.setter
    def low(self, value: float):
        self._entity.low = value

    @property
    def date(self) -> datetime.date:
        return datetime.date.fromtimestamp(self._entity.date)

    @date.setter
    def date(self, value: datetime.date):
        self._entity.date = value.timestamp()

    @property
    def high(self) -> float:
        return self._entity.high

    @high.setter
    def high(self, value: float):
        self._entity.high = value

    @property
    def open(self) -> float:
        return self._entity.open

    @open.setter
    def open(self, value: float):
        self._entity.open = value

    @property
    def close(self) -> float:
        return self._entity.close

    @close.setter
    def close(self, value: float):
        self._entity.close = value

    @property
    def volume(self) -> float:
        return self._entity.volume

    @volume.setter
    def volume(self, value: float):
        self._entity.volume = value

    @property
    def stock_id(self) -> int:
        return self._entity.stock_id

    @stock_id.setter
    def stock_id(self, value: int):
        self._entity.stock_id = value
