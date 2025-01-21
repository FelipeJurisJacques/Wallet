from .serializer import Serializer
from source.entities.historic import Historic

class Historical(Serializer):

    def __init__(self, entities: list[Historic]):
        self._entities = entities
        super().__init__()

    def handle(self):
        list = []
        for entity in self._entities:
            timeline = entity.timeline
            list.append({
                'id': entity.id,
                'date': self.serialize(timeline.datetime),
                'stock_id': timeline.stock.id,
                'low': entity.low,
                'high': entity.high,
                'open': entity.open,
                'close': entity.close,
                'volume': entity.volume,
            })
        return {
            'historical': list,
        }