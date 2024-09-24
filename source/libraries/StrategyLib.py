import math
from ..model.HistoricModel import HistoricModel
from ..model.UserStockModel import UserStockModel
from ..model.ProphesiedModel import ProphesiedModel
from ..model.UserWalletModel import UserWalletModel

class StrategyLib:
    def __init__(self):
        self._result = 0
    
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
            if first.yhat > last.close:
                print('A previsão é que a ação aumente')
                if wallet.value > last.close:
                    print('A decisão é de comprar as ações')
                    self._result = math.floor(wallet.value / last.close)
                else:
                    print('Saldo inssuficiente para comprar uma ação')
            if last.close > first.yhat:
                print('A previsão é que a ação diminua')
                if stock.value > 0:
                    print('A decisão é de vender as ações')
                    self._result = stock.value * -1
                else:
                    print('Não há ações a serem vendidas')
    
    @property
    def result(self) -> int:
        return self._result