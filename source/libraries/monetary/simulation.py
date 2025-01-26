from ..log import Log
from .wallet import Wallet
from .analyze import Analyze
from datetime import timedelta
from source.entities.stock import Stock as StockEntity
from source.enumerators.period import Period as PeriodEnum
from source.services.monetary.historic import Historic as HistoricService
from source.services.monetary.timeline import Timeline as TimelineService

class Simulation:

    def __init__(self, log: Log, money: float):
        self._decay = 3
        self._output = log
        self._analyze = Analyze(log)
        self._wallet = Wallet(money)
        self._timeline_service = TimelineService()
        self._historic_service = HistoricService()

    def handle(self):

        # obtem empresas
        stocks = StockEntity.all()
        if len(stocks) == 0:
            self._output.log('Nenhuma empresa cadastrada')
            return
        stocks = stocks[:10]

        # obtem data de inicio e fim
        start = self._timeline_service.get_min_datetime(PeriodEnum.DAY)
        if start is None:
            self._output.log('Nenhum registro a ser processado')
            return
        end = start + timedelta(days=100)
        self._output.log('Análisando ações de ' + Log.date(start) + ' até ' + Log.date(end))

        # analisa acoes das empresas
        self._analyze.set_stocks(stocks, start, end)
        self._analyze.handle()
        open_forecasts, close_forecasts, volume_forecasts = self._analyze.results()
        if len(close_forecasts) == 0:
            self._output.log('Sem opões de investimento')
            return
        self._analyze.persist()
        self._analyze.flush()

        self._output.log('Opções de investimento')
        for forecast in close_forecasts:
            self._output.log(forecast.analyze.stock.name + ' - ' + Log.date(
                    forecast.min_timeline.datetime
                ) + ' até ' + Log.date(
                    forecast.max_timeline.datetime
                ) + ' - ' + Log.percentage(
                    forecast.percentage
                )
            )

        self._output.log('Iniciando simulação')
        forecast = close_forecasts[0]
        stock = forecast.analyze.stock
        historical = self._historic_service.get_historical(
            forecast.analyze.stock,
            forecast.min_timeline.datetime,
            forecast.max_timeline.datetime
        )
        if len(historical) == 0:
            self._output.log('Fim da simulação')
            return
        for i in range(0, len(historical)):
            historic = historical[i]
            timeline = historic.timeline
            log = stock.name + '(' + Log.date(timeline.datetime) + '): ' + Log.money(historic.close)
            if i == 0:
                self._wallet.buy(historic.close)
                self._output.log(log + ' / 0.00%')
            elif i == len(historical) - 1:
                percentage = self._wallet.sell(historic.close)
                self._output.log(log + ' / ' + Log.percentage(percentage))
            else:
                self._output.log(log + ' / ' + Log.percentage(self._wallet.validate_percentage(historic.close)))
        return


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