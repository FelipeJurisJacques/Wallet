from ..entities.StockEntity import StockEntity

# MODELO DA ACAO
class StockModel:
    def __init__(self, stock: StockEntity):
        self._entity = stock

    @property
    def id(self) -> int:
        return self._entity.id

    @property
    def name(self) -> str:
        return self._entity.name

    @property
    def symbol(self) -> str:
        return self._entity.symbol

    @property
    def currency(self) -> str:
        return self._entity.currency

    @property
    def industry(self) -> str:
        return self._entity.industry