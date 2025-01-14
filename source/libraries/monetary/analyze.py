from source.services.analyze import AnalyzeService
from source.entities.forecast import ForecastEntity

class AnalyzeLib:

    def __init__(self):
        self._decay = 3
        self._service = AnalyzeService()

    def set_money(self, value):
        self._money = None
        self._fallen = None
        self._started = value
        self._quantity = None

    def set_forecast(self, forecast: ForecastEntity):
        self._fallen = None
        self._quantity = None
        self._forecast = forecast
        self._historical = self._service.get_historical(forecast)

    def handle(self):
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

    def persist(self):
        pass

    def result(self):
        return self._money
    
    def flush(self):
        del self._forecast
        del self._historical
        del self._historic_fallen
        del self._historic_applied