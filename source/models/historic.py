import datetime
from .model import Model
from ..entities.historic import HistoricEntity

class HistoricModel(Model):

    @staticmethod
    def find(id:int):
        result = HistoricEntity.objects.filter(pk=id)
        if result.exists():
            return HistoricModel(result[0])
        else:
            return None

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
    def date(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self._entity.date)

    @date.setter
    def date(self, value: datetime.datetime):
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

    @property
    def created(self) -> datetime.datetime:
        if not self._entity.created:
            return None
        else:
            return datetime.datetime.fromtimestamp(self._entity.created)

    @property
    def updated(self) -> datetime.datetime:
        if not self._entity.updated:
            return None
        else:
            return datetime.datetime.fromtimestamp(self._entity.updated)

    def save(self):        
        if not self._entity.created:
            self._entity.created = datetime.datetime.now().timestamp()
        if not self._entity.updated:
            self._entity.updated = datetime.datetime.now().timestamp()
        super().save()
