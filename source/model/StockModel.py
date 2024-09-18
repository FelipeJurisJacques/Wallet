from ..entities.StockEntity import StockEntity

class StockModel:
    def __init__(self, stock: StockEntity):
        self._entity = stock

    def getId(self):
        return self._entity.id

    def getName(self):
        return self._entity.name

    def getSymbol(self):
        return self._entity.symbol

    def getCurrency(self):
        return self._entity.currency

    def getIndustry(self):
        return self._entity.industry