from .serializer import Serializer
from source.models.stock import StockModel

class StockSerializer(Serializer):

    def __init__(self, entities: list[StockModel]):
        self._entities = entities
        super().__init__()

    def handle(self):
        list = []
        for entity in self._entities:
            list.append({
                'id': entity.id,
                'api': entity.api.name,
                'name': entity.name,
                'symbol': entity.symbol,
                'currency': entity.currency,
                'industry': entity.industry,
                'fingerprint': entity.fingerprint,
                'created': entity.created,
                'updated': entity.updated,
            })
        self._data = {
            'stocks': list,
        }