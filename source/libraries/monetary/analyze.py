import logging
from ..log import Log
from datetime import datetime
from .forecast import Forecast
from .prophet import Prophet as ProphetLib
from source.entities.stock import Stock as StockEntity
from source.enumerators.period import Period as PeriodEnum
from source.entities.analyze import Analyze as AnalyzeEntity
from source.enumerators.historic import Historic as HistoricEnum
from source.services.monetary.historic import Historic as HistoricService

class Analyze:

    def __init__(self, output: Log):
        self._output = output
        self._historic_service = HistoricService()
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
        open_forecasts = []
        close_forecasts = []
        volume_forecasts = []
        self._open_forecasts = []
        self._close_forecasts = []
        self._volume_forecasts = []

        progress = 0
        length = len(self._stocks)
        part = 100 / length
        self._output.log(f'Analisando {length} ações...')

        for stock in self._stocks:
            historical = self._historic_service.get_historical(
                stock,
                self._start,
                self._end
            )
            if len(historical) == 0:
                continue

            timelines = []
            for historic in historical:
                timelines.append(historic.timeline)
            analyze = AnalyzeEntity()
            analyze.stock = stock
            analyze.timelines = timelines
            analyze.period = PeriodEnum.MONTH

            # suprimir logs durante a execussao do profeta
            logging.getLogger('cmdstanpy').setLevel(logging.WARNING)
            logging.getLogger('prophet').setLevel(logging.WARNING)
            self._prophet.set_historical(historical)
            self._prophet.handle()
            logging.getLogger('cmdstanpy').setLevel(logging.INFO)
            logging.getLogger('prophet').setLevel(logging.INFO)

            open_prophesies, close_prophesies, volume_prophesies = self._prophet.results()
            self._prophet.flush()

            self._forecast.set_prophesies(
                open_prophesies,
                close_prophesies,
                volume_prophesies
            )
            self._forecast.handle()

            open_forecast, close_forecast, volume_forecast = self._forecast.results()
            self._forecast.flush()
            for forecast in open_forecast:
                forecast.analyze = analyze
                open_forecasts.append(forecast)
            for forecast in close_forecast:
                forecast.analyze = analyze
                close_forecasts.append(forecast)
            for forecast in volume_forecast:
                forecast.analyze = analyze
                volume_forecasts.append(forecast)
            
            progress += part
            self._output.inline(Log.percentage(progress))
        self._output.log(' COMPLETO')

        # reordena os resultados por prioridade
        if len(open_forecasts) > 0:
            self._open_forecasts = sorted(
                open_forecasts,
                key=lambda forecast: forecast.quantitative,
                reverse=True
            )
        if len(close_forecasts) > 0:
            self._close_forecasts = sorted(
                close_forecasts,
                key=lambda forecast: forecast.quantitative,
                reverse=True
            )
        if len(volume_forecasts) > 0:
            self._volume_forecasts = sorted(
                volume_forecasts,
                key=lambda forecast: forecast.quantitative,
                reverse=True
            )


    def persist(self):
        pass

    def results(self) -> tuple[
        list[Forecast], # OPEN
        list[Forecast], # CLOSE
        list[Forecast], # VOLUME
    ]:
        return self._open_forecasts, self._close_forecasts, self._volume_forecasts
    
    def flush(self):
        del self._end
        del self._start
        del self._stocks
        del self._open_forecasts
        del self._close_forecasts
        del self._volume_forecasts