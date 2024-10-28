import datetime
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
        return HistoricDayEntity(self._model.last_historic_id)

    @last_historic.setter
    def last_historic(self, value: HistoricDayEntity):
        self._model.last_historic_id = value._model

    @property
    def last_historic_id(self) -> int:
        return self._model.last_historic_id.id

    @property
    def open(self) -> ProphesyEntity:
        return ProphesyEntity(self._model.open_prophesy_id)

    @open.setter
    def open(self, value: ProphesyEntity):
        self._model.open_prophesy_id = value._model

    @property
    def open_prophesy_id(self) -> int:
        return self._model.open_prophesy_id.id

    @property
    def close(self) -> ProphesyEntity:
        return ProphesyEntity(self._model.close_prophesy_id)

    @close.setter
    def close(self, value: ProphesyEntity):
        self._model.close_prophesy_id = value._model

    @property
    def close_prophesy_id(self) -> int:
        return self._model.close_prophesy_id.id

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
