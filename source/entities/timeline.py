from datetime import datetime
from ..entities.stock import Stock
from ..enumerators.period import Period as PeriodEnum
from ..models.timeline import Timeline as TimelineModel

class Timeline:

    @staticmethod
    def find(id:int):
        result = TimelineModel.objects.filter(pk=id)
        if result.exists():
            return Timeline(result[0])
        else:
            return None

    def __init__(self, model: TimelineModel = None):
        if model is None:
            self._model = TimelineModel()
        else:
            self._model = model

    @property
    def id(self) -> int:
        return self._model.id

    @property
    def stock(self) -> Stock:
        return Stock(self._model.stock)

    @stock.setter
    def stock(self, value: Stock):
        self._model.stock = value._model
    
    @property
    def type(self) -> PeriodEnum:
        return PeriodEnum(self._model.type)

    @type.setter
    def type(self, value: PeriodEnum):
        self._model.type = value.value

    @property
    def working(self) -> bool:
        return self._model.working == 1

    @working.setter
    def working(self, value: bool):
        if value:
            self._model.working = 1
        else:
            self._model.working = 0

    @property
    def datetime(self) -> datetime:
        return datetime.fromtimestamp(self._model.datetime)

    @datetime.setter
    def datetime(self, value: datetime):
        self._model.datetime = value.timestamp()

    def save(self):
        self._model.save()