from .entity import Entity
from .timeline import Timeline
from ..models.historic import Historic as HistoricModel

class Historic(Entity):

    @staticmethod
    def find(id:int):
        result = HistoricModel.objects.filter(pk=id)
        if result.exists():
            return Historic(result[0])
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
    def timeline(self) -> Timeline:
        return Timeline(self._model.timeline)

    @timeline.setter
    def timeline(self, value: Timeline):
        self._model.timeline = value._model

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
