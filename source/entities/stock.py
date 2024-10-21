import json
import datetime
from .entity import Entity
from ..enumerators.api import ApiEnum
from ..models.stock import StockModel

class StockEntity(Entity):

    @staticmethod
    def find(id:int):
        result = StockModel.objects.filter(pk=id)
        if result.exists():
            return StockEntity(result[0])
        else:
            return None

    def __init__(self, model: StockModel = None):
        if model is None:
            self._model = StockModel()
        else:
            self._model = model

    @property
    def id(self) -> int:
        return self._model.id

    @property
    def api(self) -> ApiEnum:
        return ApiEnum(self._model.api)

    @api.setter
    def api(self, value: ApiEnum):
        self._model.api = value.value

    @property
    def name(self) -> str:
        return self._model.name

    @name.setter
    def name(self, value: str):
        self._model.name = value

    @property
    def symbol(self) -> str:
        return self._model.symbol

    @symbol.setter
    def symbol(self, value: str):
        self._model.symbol = value

    @property
    def currency(self) -> str:
        return self._model.currency

    @currency.setter
    def currency(self, value: str):
        self._model.currency = value

    @property
    def industry(self) -> str:
        return self._model.industry

    @industry.setter
    def industry(self, value: str):
        self._model.industry = value
    
    @property
    def fingerprint(self) -> object:
        if not self._model.fingerprint:
            return None
        else:
            return json.loads(self._model.fingerprint)

    @fingerprint.setter
    def fingerprint(self, value: object):
        self._model.fingerprint = json.dumps(value)

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
        if not self._model.fingerprint:
            self._model.fingerprint = '{}'
        if not self._model.created:
            self._model.created = datetime.datetime.now().timestamp()
        if not self._model.updated:
            self._model.updated = datetime.datetime.now().timestamp()
        super().save()