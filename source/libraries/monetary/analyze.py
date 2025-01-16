from datetime import datetime
from .forecast import Forecast
from .prophet import Prophet as ProphetLib
from source.entities.stock import Stock as StockEntity
from source.enumerators.period import Period as PeriodEnum
from source.enumerators.historic import Historic as HistoricEnum
from source.services.monetary.analyze import Analyze as AnalyzeService

class Analyze:

    def __init__(self):
        self._service = AnalyzeService()
        self._prophet = ProphetLib([
            HistoricEnum.CLOSE,
        ], PeriodEnum.MONTH)
        self._forecast = Forecast()

    def set_stocks(
        self,
        stocks: list[StockEntity],
        start: datetime,
        end: datetime
    ):
        self._end = end
        self._start = start
        self._stocks = stocks

    def handle(self):
        for stock in self._stocks:
            historical = self._service.get_historical(
                stock,
                self._start,
                self._end
            )
            if len(historical) == 0:
                continue
            self._prophet.set_historical(historical)
            self._prophet.handle()
            open_prophesies, close_prophesies, volume_prophesies = self._prophet.results()
            self._forecast.set_prophesies(
                open_prophesies,
                close_prophesies,
                volume_prophesies
            )
            self._forecast.handle()
            open_forecast, close_forecast, volume_forecast = self._forecast.results()

    def persist(self):
        pass

    def result(self):
        pass
    
    def flush(self):
        del self._stocks
        self._prophet.flush()
        self._forecast.flush()