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
        self._fails = 0
        self._total = 0
        self._decay = 2.0
        self._success = 0
        self._output = log
        self._money = money
        self._rampant = True
        self._analyze = Analyze(log)
        self._timeline_service = TimelineService()
        self._historic_service = HistoricService()

    def handle(self):

        # obtem empresas
        stocks = StockEntity.all()
        if len(stocks) == 0:
            self._output.log('Nenhuma empresa cadastrada')
            return
        # stocks = stocks[:5]

        # obtem data de inicio e fim
        start = self._timeline_service.get_min_datetime(PeriodEnum.DAY)
        if start is None:
            self._output.log('Nenhum registro a ser processado')
            return
        end = start + timedelta(days=100)

        if self._rampant:
            self._wallet = Wallet(self._money)

        next = True
        while next:
            self._output.log('Análisando ações de ' + Log.date(start) + ' até ' + Log.date(end))

            # analisa acoes das empresas
            self._analyze.set_stocks(stocks, start, end)
            self._analyze.handle()
            open_forecasts, close_forecasts, volume_forecasts = self._analyze.results()
            # self._analyze.persist()
            self._analyze.flush()
            if len(close_forecasts) == 0:
                self._output.log('Sem opões de investimento')
                if self._rampant:
                    end = end + timedelta(days=30)
                    start = start + timedelta(days=30)
                    continue
                else:
                    break

            if self._rampant:
                self._total += 1
                forecast = close_forecasts[0]
                stock = forecast.analyze.stock
                self._output.log(stock.name + ' - ' + Log.date(
                        forecast.min_timeline.datetime
                    ) + ' até ' + Log.date(
                        forecast.max_timeline.datetime
                    ) + ' - ' + Log.percentage(
                        forecast.percentage
                    )
                )
                historical = self._historic_service.get_historical(
                    stock,
                    forecast.min_timeline.datetime,
                    forecast.max_timeline.datetime
                )
                if len(historical) == 0:
                    self._output.log('Fim da simulação')
                    break
                self._output.log('Simulando ' + stock.name)
                decay = self._decay * -1.0
                for i in range(0, len(historical)):
                    historic = historical[i]
                    timeline = historic.timeline
                    log = Log.date(timeline.datetime) + ': ' + Log.money(historic.close)
                    if i == 0:
                        self._wallet.buy(historic.close)
                        self._output.log(log + ' / 0.00%')
                    else:
                        value = historic.open
                        percentage = self._wallet.validate_percentage(value)
                        if percentage < forecast.percentage:
                            value = historic.close
                            percentage = self._wallet.validate_percentage(value)
                        value = historic.close
                        percentage = self._wallet.validate_percentage(value)
                        if i == len(historical) - 1 or percentage > forecast.percentage or decay > percentage:
                            end = timeline.datetime
                            start = end - timedelta(days=100)
                            percentage = self._wallet.sell(value)
                            self._output.log(log + ' / ' + Log.percentage(percentage))
                            if percentage > 0:
                                self._success += 1
                            else:
                                self._fails += 1
                            break
                        else:
                            self._output.log(log + ' / ' + Log.percentage(percentage))
                self._output.log(f'Acumulado: {Log.money(self._wallet.money)}')
                percentage = (self._success / self._total) * 100
                self._output.log(f'Sucesso: {self._success} / Falhas: {self._fails} / Total: {self._total} / Porcentagem: {Log.percentage(percentage)}')
            else:
                next = False
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

                self._total += len(close_forecasts)
                self._output.log('Iniciando simulação')
                for forecast in close_forecasts:
                    self._wallet = Wallet(self._money)
                    stock = forecast.analyze.stock
                    historical = self._historic_service.get_historical(
                        forecast.analyze.stock,
                        forecast.min_timeline.datetime,
                        forecast.max_timeline.datetime
                    )
                    if len(historical) == 0:
                        self._output.log('Fim da simulação')
                        return
                    self._output.log('Simulando ' + stock.name)
                    for i in range(0, len(historical)):
                        historic = historical[i]
                        timeline = historic.timeline
                        log = Log.date(timeline.datetime) + ': ' + Log.money(historic.close)
                        if i == 0:
                            self._wallet.buy(historic.close)
                            self._output.log(log + ' / 0.00%')
                        elif i == len(historical) - 1:
                            percentage = self._wallet.sell(historic.close)
                            self._output.log(log + ' / ' + Log.percentage(percentage))
                            if percentage > 0:
                                self._success += 1
                            else:
                                self._fails += 1
                        else:
                            self._output.log(log + ' / ' + Log.percentage(self._wallet.validate_percentage(historic.close)))

        percentage = (self._success / self._total) * 100
        self._output.log(f'Sucesso: {self._success} / Falhas: {self._fails} / Total: {self._total} / Porcentagem: {Log.percentage(percentage)}')
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