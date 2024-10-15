from .serializer import Serializer
from source.models.historic import HistoricModel

class HistoricalSerializer(Serializer):

    def __init__(self, entities: list[HistoricModel]):
        self._entities = entities
        super().__init__()

    def handle(self):
        list = []
        for entity in self._entities:
            list.append({
                'id': entity.id,
                'date': entity.date.isoformat(),
                'stock_id': entity.stock_id,
                'low': entity.low,
                'high': entity.high,
                'open': entity.open,
                'close': entity.close,
                'volume': entity.volume,
            })
        return {
            'historical': list,
        }