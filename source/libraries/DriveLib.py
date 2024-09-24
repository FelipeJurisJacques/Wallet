import math
from ..model.UserStockModel import UserStockModel
from ..model.UserWalletModel import UserWalletModel

class DriveLib:
    def __init__(self):
        # teste em memoria
        self._userStock = None
        self._userWallet = None

    def getUserStock(self) -> UserStockModel:
        # teste em memoria
        if self._userStock is None:
            self._userStock = UserStockModel()
        return self._userStock

    def getUserWallet(self) -> UserWalletModel:
        # teste em memoria
        if self._userStock is None:
            self._userWallet = UserWalletModel()
        return self._userWallet
    
    def buyable(self, value: float) -> int:
        if value > 0.0:
            wallet = self.getUserWallet()
            if wallet.value > 0.0:
                return math.floor(wallet.value / value)
        return 0
    
    def sellable(self) -> int:
        return self.getUserStock().value

    def buy(self, value: float, quantity: int) -> bool:
        if value > 0.0 and quantity > 0:
            total = quantity * value
            wallet = self.getUserWallet()
            if wallet.value > total:
                result = self.getUserStock()
                wallet.value -= total
                result.value += quantity
                return True
        return False

    def sell(self, value: float, quantity: int) -> bool:
        if value > 0.0 and quantity > 0:
            result = self.getUserStock()
            if result.value >= quantity:
                wallet = self.getUserWallet()
                total = quantity * value
                wallet.value += total
                result.value -= quantity
                return True
        return False