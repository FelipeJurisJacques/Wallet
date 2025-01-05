import json
import pytz
import datetime
from .entity import Entity
from ..enumerators.api import ApiEnum
from ..models.stock import StockModel

class StockEntity(Entity):

    @staticmethod
    def all():
        result = []
        for model in StockModel.objects.all():
            result.append(StockEntity(model))
        return result

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
    def timezone(self) -> datetime.timezone:
        for tz_name in pytz.all_timezones:
            tz = pytz.timezone(tz_name)
            now = datetime.datetime.now(tz)
            offset = now.utcoffset()
            if offset is not None and offset.total_seconds() / 3600 == self._model.timezone:
                return tz
        return None

    @timezone.setter
    def timezone(self, value: datetime.timezone):
        current_time = datetime.datetime.now(value)
        self._model.timezone = current_time.utcoffset().total_seconds() / 3600
    
    @property
    def fingerprint(self) -> object:
        if not self._model.fingerprint:
            return None
        else:
            return json.loads(self._model.fingerprint)

    @fingerprint.setter
    def fingerprint(self, value: object):
        self._model.fingerprint = json.dumps(value)

    def save(self):        
        if not self._model.fingerprint:
            self._model.fingerprint = '{}'
        super().save()