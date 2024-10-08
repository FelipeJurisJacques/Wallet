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
        
    # Stop-loss: Vender ações automaticamente quando caem abaixo de um certo valor.
    # Take-profit: Vender ações quando atingem um valor predeterminado de ganho.
    
    def handle(
        self,
        wallet: UserWalletModel,
        stock: UserStockModel,
        last: HistoricModel,
        forecast: ProphesiedModel,
        compare: HistoricModel = None
    ):
        self._result = 0
        percentage = str(round(self.estimatePercent(last.close, forecast.yhat), 2)) + '%'
        if forecast.yhat > last.close:
            if compare is None:
                print('A previsão é que a ação aumente em ' + percentage)
            if wallet.value > last.close:
                self._result = math.floor(wallet.value / last.close)
                print('A decisão é de comprar ' + str(self._result) + ' ações')
            else:
                print('Saldo inssuficiente para comprar uma ação')
        if last.close > forecast.yhat:
            if compare is None:
                print('A previsão é que a ação diminua em ' + percentage)
            if stock.value > 0:
                self._result = stock.value * -1
                print('A decisão é de vender ' + str(self._result) + ' ações')
            else:
                print('Não há ações a serem vendidas')
        if not compare is None:
            real = str(round(self.estimatePercent(last.close, compare.close), 2)) + '%'
            print('Percentual previsto ' + percentage + ' e verdadeiro ' + real)
    
    @property
    def result(self) -> int:
        return self._result