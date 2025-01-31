from ..log import Log
from .prophet import Prophet
from datetime import datetime
from .forecast import Forecast
from source.entities.stock import Stock as StockEntity
from source.enumerators.period import Period as PeriodEnum
from source.entities.analyze import Analyze as AnalyzeEntity
from source.enumerators.context import Context as ContextEnum
from source.libraries.database.transaction import Transaction
from source.enumerators.historic import Historic as HistoricEnum
from source.services.monetary.historic import Historic as HistoricService

class Analyze:

    def __init__(self, output: Log, context: ContextEnum):
        self._output = output
        self._context = context
        self._historic_service = HistoricService()
        self._forecast = Forecast()
        self._transaction = Transaction()

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
        self._analyzes = []
        open_forecasts = []
        close_forecasts = []
        self._open_forecasts = []
        self._close_forecasts = []
        self._open_prophesies = []
        self._close_prophesies = []
        self._volume_prophesies = []

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

            # suprimir logs durante a execussao do profeta
            prophet = Prophet(
                type=HistoricEnum.CLOSE,
                input_period=PeriodEnum.DAY,
                output_period=PeriodEnum.MONTH
            )
            prophet.set_historical(historical)
            prophet.handle()
            prophesies = prophet.results()
            prophet.flush()
            if len(prophesies) == 0:
                continue
            
            # analize
            timelines = []
            for historic in historical:
                timelines.append(historic.timeline)
            analyze = AnalyzeEntity()
            analyze.stock = stock
            analyze.timelines = timelines
            analyze.context = self._context
            analyze.period = PeriodEnum.MONTH
            self._analyzes.append(analyze)
            for prophesy in prophesies:
                prophesy.analyze = analyze
                self._close_prophesies.append(prophesy)

            self._forecast.set_close_prophesies(prophesies)
            self._forecast.handle()

            open_forecast, close_forecast = self._forecast.results()
            self._forecast.flush()
            for forecast in open_forecast:
                forecast.analyze = analyze
                open_forecasts.append(forecast)
            for forecast in close_forecast:
                forecast.analyze = analyze
                close_forecasts.append(forecast)

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

    def persist(self):
        try:
            self._transaction.begin()
            for analyze in self._analyzes:
                analyze.save()
            for prophesy in self._open_prophesies:
                prophesy.save()
            for prophesy in self._close_prophesies:
                prophesy.save()
            for prophesy in self._volume_prophesies:
                prophesy.save()
            for forecast in self._open_forecasts:
                forecast.save()
            for forecast in self._close_forecasts:
                forecast.save()
            self._transaction.commit()
        except Exception as error:
            self._transaction.rollback()
            raise error

    def results(self) -> tuple[
        list[Forecast], # OPEN
        list[Forecast], # CLOSE
    ]:
        return self._open_forecasts, self._close_forecasts
    
    def flush(self):
        del self._end
        del self._start
        del self._stocks
        del self._analyzes
        del self._open_forecasts
        del self._close_forecasts
        del self._open_prophesies
        del self._close_prophesies
        del self._volume_prophesies