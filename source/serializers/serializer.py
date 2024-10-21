import datetime
from enum import Enum

class Serializer:

    def __init__(self, input = None):
        self._input = input
        self._output = self.handle()

    def handle(self) -> str:
        return self.serialize(self._input)
    
    def serialize(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            return value
        if isinstance(value, int):
            return value
        if isinstance(value, bool):
            return value
        if isinstance(value, float):
            return value
        if isinstance(value, Enum):
            return value.name
        if isinstance(value, datetime.date):
            return value.isoformat() + 'Z'
        if isinstance(value, datetime.time):
            return value.isoformat() + 'Z'
        if isinstance(value, datetime.datetime):
            return value.isoformat() + 'Z'
        if isinstance(value, list):
            result = []
            for v in value:
                result.append(self.serialize(v))
            return result
        if isinstance(value, object):
            # attributes = vars(value)
            if hasattr(value, '__dict__'):
                keys = []
                values = []
                attributes = dir(value)
                for key in attributes:
                    if key.find("_") == 0:
                        continue
                    if not hasattr(value, key):
                        continue
                    attribute = getattr(value, key)
                    if callable(attribute):
                        continue
                    keys.append(key)
                    values.append(self.serialize(attribute))
                return {**dict(zip(keys, values))}
        return value

    @property
    def data(self):
        return self._output