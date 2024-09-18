import datetime
from ..entities.HistoricEntity import HistoricEntity

class HistoricModel:
    def __init__(self, historic: HistoricEntity):
        self._entity = historic

    @property
    def id(self) -> int:
        return self._entity.id

    @property
    def low(self) -> float:
        return self._entity.low

    @property
    def date(self) -> datetime.date:
        return datetime.date.fromtimestamp(self._entity.date)

    @property
    def high(self) -> float:
        return self._entity.high

    @property
    def open(self) -> float:
        return self._entity.open

    @property
    def close(self) -> float:
        return self._entity.close

    @property
    def volume(self) -> float:
        return self._entity.volume

    @property
    def stockId(self) -> int:
        return self._entity.stock_id
