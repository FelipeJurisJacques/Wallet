from .serializer import Serializer
from source.entities.historic_day import HistoricDayEntity

class HistoricalSerializer(Serializer):

    def __init__(self, models: list[HistoricDayEntity]):
        self._models = models
        super().__init__()

    def handle(self):
        list = []
        for model in self._models:
            list.append({
                'id': model.id,
                'date': model.date.isoformat() + 'Z',
                'stock_id': model.stock_id,
                'low': model.low,
                'high': model.high,
                'open': model.open,
                'close': model.close,
                'volume': model.volume,
            })
        return {
            'historical': list,
        }