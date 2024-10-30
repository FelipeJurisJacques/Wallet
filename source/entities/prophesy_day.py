from .entity import Entity
from .prophesy import ProphesyEntity
from ..models.prophesy_day import ProphesyDayModel
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
    def last_historic(self) -> HistoricDayEntity:
        return HistoricDayEntity(self._model.last_historic)

    @last_historic.setter
    def last_historic(self, value: HistoricDayEntity):
        self._model.last_historic = value._model

    @property
    def open(self) -> ProphesyEntity:
        return ProphesyEntity(self._model.open_prophesy)

    @open.setter
    def open(self, value: ProphesyEntity):
        self._model.open_prophesy = value._model

    @property
    def close(self) -> ProphesyEntity:
        return ProphesyEntity(self._model.close_prophesy)

    @close.setter
    def close(self, value: ProphesyEntity):
        self._model.close_prophesy = value._model
