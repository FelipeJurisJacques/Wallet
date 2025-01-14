from datetime import timedelta
from .prophet import Prophet as ProphetLib
from .forecast import Forecast as ForecastLib
from source.entities.stock import Stock as StockEntity
from source.enumerators.period import Period as PeriodEnum
from source.enumerators.historic import Historic as HistoricEnum
from source.services.monetary.simulation import Simulation as SimulationService

class Simulation:

    def __init__(self):
        self._service = SimulationService()
        self._prophet = ProphetLib([
            HistoricEnum.CLOSE,
        ], PeriodEnum.MONTH)
        self._forecast = ForecastLib()

    def handle(self):
        start = self._service.get_historic_start_date()
        if start is not None:
            end = start + timedelta(days=180)
            stocks = StockEntity.all()
            stop = True
            for stock in stocks:
                historical = self._service.get_historical(stock, start, end)
                if len(historical) == 0:
                    continue
                stop = False
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

