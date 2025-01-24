class Wallet:

    def __init__(self, money: float):
        self._applied = 0
        self._quantity = 0
        self._money = money

    @property
    def money(self):
        return self._money

    @property
    def quantity(self):
        return self._quantity

    @property
    def applied(self):
        return self._quantity > 0

    def buy(self, stock_value: float, quantity: int = None):
        if quantity is None:
            self._quantity += self._money / stock_value
            applied = stock_value * self._quantity
            self._applied += applied
            self._money -= self._applied
        elif quantity * stock_value > self._money:
            applied = stock_value * quantity
            self._applied += applied
            self._money -= self._applied
            self._quantity += quantity
        else:
            raise Exception('Not enough money')

    def sell(self, stock_value: float, quantity: int = None):
        percentage = self.validate_percentage(stock_value)
        if quantity is None:
            self._money += stock_value * self._quantity
            self._applied = 0
            self._quantity = 0
        elif quantity > self._quantity:
            collected = stock_value * quantity
            self._money += collected
            self._applied -= collected
            self._quantity -= quantity
        else:
            raise Exception('Not enough quantity')
        return percentage

    def validate_percentage(self, stock_value: float):
        if self._quantity == 0:
            raise Exception('No stocks')
        value = self._quantity * stock_value
        delta = (value - self._applied) / self._applied
        return delta * 100
        