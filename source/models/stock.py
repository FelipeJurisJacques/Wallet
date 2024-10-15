import json
import datetime
from .model import Model
from ..enumerators.api import ApiEnum
from ..entities.stock import StockEntity

class StockModel(Model):

    @staticmethod
    def find(id:int) -> StockEntity:
        result = StockEntity.objects.filter(pk=id)
        if result.exists():
            return StockModel(result[0])
        else:
            return None

    def __init__(self, entity: StockEntity = None):
        if entity is None:
            self._entity = StockEntity()
        else:
            self._entity = entity

    @property
    def id(self) -> int:
        return self._entity.id

    @property
    def api(self) -> ApiEnum:
        return ApiEnum(self._entity.api)

    @api.setter
    def api(self, value: ApiEnum):
        self._entity.api = value.value

    @property
    def name(self) -> str:
        return self._entity.name

    @name.setter
    def name(self, value: str):
        self._entity.name = value

    @property
    def symbol(self) -> str:
        return self._entity.symbol

    @symbol.setter
    def symbol(self, value: str):
        self._entity.symbol = value

    @property
    def currency(self) -> str:
        return self._entity.currency

    @currency.setter
    def currency(self, value: str):
        self._entity.currency = value

    @property
    def industry(self) -> str:
        return self._entity.industry

    @industry.setter
    def industry(self, value: str):
        self._entity.industry = value
    
    @property
    def fingerprint(self) -> object:
        if not self._entity.fingerprint:
            return None
        else:
            return json.loads(self._entity.fingerprint)

    @fingerprint.setter
    def fingerprint(self, value: object):
        self._entity.fingerprint = json.dumps(value)

    @property
    def created(self) -> datetime.datetime:
        if not self._entity.created:
            return None
        else:
            return datetime.datetime.fromtimestamp(self._entity.created)

    @property
    def updated(self) -> datetime.datetime:
        if not self._entity.updated:
            return None
        else:
            return datetime.datetime.fromtimestamp(self._entity.updated)

    def save(self):        
        if not self._entity.fingerprint:
            self._entity.fingerprint = '{}'
        if not self._entity.created:
            self._entity.created = datetime.datetime.now().timestamp()
        if not self._entity.updated:
            self._entity.updated = datetime.datetime.now().timestamp()
        super().save()