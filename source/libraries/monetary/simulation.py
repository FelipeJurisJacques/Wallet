from .analyze import Analyze
from datetime import timedelta
from source.entities.stock import Stock as StockEntity
from source.services.monetary.simulation import Simulation as SimulationService

class Simulation:

    def __init__(self):
        self._decay = 3
        self._money = None
        self._fallen = None
        self._started = 1000
        self._quantity = None
        self._analyze = Analyze()
        self._service = SimulationService()

    def handle(self):
        stocks = StockEntity.all()
        start = self._service.get_historic_start_date()
        if start is not None:
            end = start + timedelta(days=180)
            self._analyze.set_stocks(stocks, start, end)
            self._analyze.handle()
            self._analyze.result()
            self._analyze.flush()
        money = None
        self._historic_fallen = None
        self._historic_applied = None
        historic = self._historical[0]
        limit = self._forecast.max_date
        expected = self._forecast.max_value
        if self._money is None:
            money = self._started
        else:
            money = self._money
        quantity = round(money / historic.close)
        money = quantity * historic.close
        self._fallen = money * ((100 - self._decay) / 100)
        for historic in self._historical:
            money = quantity * historic.close
            if self._fallen >= money:
                self._historic_fallen = historic
                break
            if money >= expected or historic.date >= limit:
                self._historic_applied = historic
                break
        self._money = money
        self._quantity = quantity
    
    def flush(self):
        del self._forecast
        del self._historical
        del self._historic_fallen
        del self._historic_applied