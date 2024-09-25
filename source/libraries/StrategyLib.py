import math
from ..model.HistoricModel import HistoricModel
from ..model.UserStockModel import UserStockModel
from ..model.ProphesiedModel import ProphesiedModel
from ..model.UserWalletModel import UserWalletModel

class StrategyLib:
    def __init__(self):
        self._result = 0
    
    def estimatePercent(self, actual: float, forecast: float):
        if forecast != actual:
            return ((forecast - actual) * 100) / actual
        else:
            return 0
    
    def handle(
        self,
        wallet: UserWalletModel,
        stock: UserStockModel,
        historical: list[HistoricModel],
        forecast: list[ProphesiedModel]
    ):
        self._result = 0
        if len(historical) > 0 and len(forecast) > 0:
            last = historical[-1]
            first = forecast[0]
            percentage = str(round(self.estimatePercent(last.close, first.yhat), 2)) + '%'
            if first.yhat > last.close:
                print('A previsão é que a ação aumente em ' + percentage)
                if wallet.value > last.close:
                    self._result = math.floor(wallet.value / last.close)
                    print('A decisão é de comprar ' + str(self._result) + ' ações')
                else:
                    print('Saldo inssuficiente para comprar uma ação')
            if last.close > first.yhat:
                print('A previsão é que a ação diminua em ' + percentage)
                if stock.value > 0:
                    self._result = stock.value * -1
                    print('A decisão é de vender ' + str(self._result) + ' ações')
                else:
                    print('Não há ações a serem vendidas')
    
    @property
    def result(self) -> int:
        return self._result