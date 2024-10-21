import datetime
from ..entities.Entity import Entity

# MODELO CARTEIRA
class UserWalletModel:
    def __init__(self, entity: Entity = None):
        if entity is None:
            self._entity = Entity(
                value=0
            )
        else:
            self._entity = entity

    @property
    def id(self) -> int:
        return self._entity.id

    @id.setter
    def id(self, value: int):
        self._entity.id = value

    @property
    def value(self) -> float:
        return self._entity.value

    @value.setter
    def value(self, value: float):
        self._entity.value = value

    @property
    def currency(self) -> str:
        return self._entity.currency

    @currency.setter
    def created(self, value: str):
        self._entity.currency = value

    @property
    def created(self) -> datetime.datetime:
        return datetime.created.fromtimestamp(self._entity.date)

    @created.setter
    def created(self, value: datetime.datetime):
        self._entity.created = value.timestamp()

    @property
    def updated(self) -> datetime.datetime:
        return datetime.updated.fromtimestamp(self._entity.date)

    @updated.setter
    def updated(self, value: datetime.datetime):
        self._entity.updated = value.timestamp()