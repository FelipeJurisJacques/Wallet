from .entity import Entity
from datetime import datetime
from ..entities.stock import StockEntity
from ..models.historic import HistoricModel
from ..enumerators.period import PeriodEnum

class HistoricEntity(Entity):

    @staticmethod
    def find(id:int):
        result = HistoricModel.objects.filter(pk=id)
        if result.exists():
            return HistoricEntity(result[0])
        else:
            return None

    def __init__(self, model: HistoricModel = None):
        if model is None:
            self._model = HistoricModel()
        else:
            self._model = model

    @property
    def id(self) -> int:
        return self._model.id

    @property
    def stock(self) -> StockEntity:
        return StockEntity(self._model.stock)

    @stock.setter
    def stock(self, value: StockEntity):
        self._model.stock = value._model
    
    @property
    def type(self) -> PeriodEnum:
        return PeriodEnum(self._model.type)

    @type.setter
    def type(self, value: PeriodEnum):
        self._model.type = value.value

    @property
    def date(self) -> datetime:
        return datetime.fromtimestamp(self._model.date)

    @date.setter
    def date(self, value: datetime):
        self._model.date = value.timestamp()

    @property
    def low(self) -> float:
        return self._model.low

    @low.setter
    def low(self, value: float):
        self._model.low = value

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
    def volume(self) -> int:
        return self._model.volume

    @volume.setter
    def volume(self, value: int):
        self._model.volume = value
