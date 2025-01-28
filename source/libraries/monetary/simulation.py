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
        self._days = 100
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
        end = start + timedelta(days=self._days)

        if self._rampant:
            self._wallet = Wallet(self._money)

        next = True
        while next:
            self._output.log('Análisando ações de ' + Log.date(start) + ' até ' + Log.date(end))

            # analisa acoes das empresas
            self._analyze.set_stocks(stocks, start, end)
            self._analyze.handle()
            open_forecasts, close_forecasts, volume_forecasts = self._analyze.results()
            self._analyze.persist()
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
                profit = int(forecast.percentage) / 2.0
                for i in range(0, len(historical)):
                    historic = historical[i]
                    timeline = historic.timeline
                    log = Log.date(timeline.datetime) + ': ' + Log.money(historic.close)
                    if i == 0:
                        self._wallet.buy(historic.close)
                        self._output.log(log + ' / 0.00%')
                    else:
                        apply = False
                        value = historic.close
                        open_percentage = self._wallet.validate_percentage(historic.open)
                        close_percentage = self._wallet.validate_percentage(historic.close)
                        if 0.0 > open_percentage or 0.0 > close_percentage:
                            profit = 0.2
                        if open_percentage > profit or decay > open_percentage:
                            apply = True
                            value = historic.close
                        if close_percentage > profit or decay > close_percentage:
                            apply = True
                        if i == len(historical) - 1:
                            apply = True
                        if apply:
                            end = timeline.datetime
                            start = end - timedelta(days=self._days)
                            percentage = self._wallet.sell(value)
                            self._output.log(log + ' / ' + Log.percentage(percentage))
                            if percentage > 0:
                                self._success += 1
                            else:
                                self._fails += 1
                            break
                        else:
                            self._output.log(log + ' / ' + Log.percentage(close_percentage))
                self._output.log(f'Acumulado: {Log.money(self._wallet.money)}')
                percentage = (self._success / self._total) * 100
                self._output.log(f'Sucesso: {self._success} / Falhas: {self._fails} / Total: {self._total} / Porcentagem: {Log.percentage(percentage)}')
            else:
                next = False
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
                    self._output.log(stock.name + ' - ' + Log.date(
                            forecast.min_timeline.datetime
                        ) + ' até ' + Log.date(
                            forecast.max_timeline.datetime
                        ) + ' - ' + Log.percentage(
                            forecast.percentage
                        )
                    )
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
    
    def flush(self):
        del self._forecast
        del self._historical
        del self._historic_fallen
        del self._historic_applied