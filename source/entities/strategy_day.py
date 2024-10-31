from .entity import Entity
from .historic_day import HistoricDayEntity
from ..models.strategy_day import StrategyDayModel

class StrategyDayEntity(Entity):

    @staticmethod
    def find(id:int):
        result = StrategyDayModel.objects.filter(pk=id)
        if result.exists():
            return StrategyDayEntity(result[0])
        else:
            return None

    def __init__(self, model: StrategyDayModel = None):
        if model is None:
            self._model = StrategyDayModel()
        else:
            self._model = model

    @property
    def id(self) -> int:
        return self._model.id

    @property
    def historic(self) -> HistoricDayEntity:
        return HistoricDayEntity(self._model.historic)

    @historic.setter
    def historic(self, value: HistoricDayEntity):
        self._model.historic = value._model
    
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