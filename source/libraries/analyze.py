from ..services.analyze import AnalyzeService
from ..entities.forecast import ForecastEntity

class AnalyzeLib:

    def __init__(self):
        self._decay = 3
        self._service = AnalyzeService()

    def set_money(self, value):
        self._money = value

    def set_forecast(self, forecast: ForecastEntity):
        self._forecast = forecast
        self._historical = self._service.get_historical(forecast)

    def handle(self):
        historic = self._historical[0]
        limit = self._forecast.max_date
        expected = self._forecast.max_value
        self._quantity = round(self._money / historic.close)
        self._started = self._quantity * historic.close
        self._fallen = self._started * ((100 - self._decay) / 100)
        for historic in self._historical:
            self._result = self._quantity * historic.close
            if self._fallen >= self._result or self._result >= expected or historic.date >= limit:
                self._historic_applied = historic
                break

    def persist(self):
        return self._result
    
    def flush(self):
        del self._money
        del self._result
        del self._fallen
        del self._started
        del self._forecast
        del self._quantity
        del self._historical
        del self._historic_applied