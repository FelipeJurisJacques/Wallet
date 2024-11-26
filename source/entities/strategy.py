from .entity import Entity
from .period import PeriodEntity
from ..models.strategy import StrategyModel

class StrategyDayEntity(Entity):

    @staticmethod
    def find(id:int):
        result = StrategyModel.objects.filter(pk=id)
        if result.exists():
            return StrategyDayEntity(result[0])
        else:
            return None

    def __init__(self, model: StrategyModel = None):
        if model is None:
            self._model = StrategyModel()
        else:
            self._model = model

    @property
    def id(self) -> int:
        return self._model.id
    
    @property
    def period(self) -> PeriodEntity:
        return PeriodEntity(self._model.period)

    @period.setter
    def period(self, value: PeriodEntity):
        self._model.period = value._model
    
    @property
    def qualitative(self) -> float:
        return self._model.qualitative

    @qualitative.setter
    def qualitative(self, value: float):
        self._model.qualitative = value

    @property
    def quantitative(self) -> float:
        return self._model.quantitative

    @quantitative.setter
    def quantitative(self, value: float):
        self._model.quantitative = value