from ..log import Log
from .analyze import Analyze
from .prophet import Prophet
from datetime import timedelta
from source.entities.stock import Stock as StockEntity
from source.enumerators.period import Period as PeriodEnum
from source.entities.analyze import Analyze as AnalyzeEntity
from source.enumerators.context import Context as ContextEnum
from source.libraries.database.transaction import Transaction
from source.enumerators.historic import Historic as HistoricEnum
from source.services.monetary.historic import Historic as HistoricService
from source.services.monetary.timeline import Timeline as TimelineService

class TrainProphesy:

    def __init__(self, log: Log):
        self._fails = 0
        self._total = 0
        self._days = 100
        self._decay = 2.0
        self._cycles = 10
        self._success = 0
        self._output = log
        self._rampant = True
        self._analyze = Analyze(log)
        self._transaction = Transaction()
        self._timeline_service = TimelineService()
        self._historic_service = HistoricService()
        self._prophet = Prophet(HistoricEnum.CLOSE, PeriodEnum.DAY)

    def handle(self):

        # obtem empresas
        stocks = StockEntity.all()
        if len(stocks) == 0:
            self._output.log('Nenhuma empresa cadastrada')
            return
        # stocks = stocks[:2]

        period = PeriodEnum.MONTH
        start = self._timeline_service.get_min_datetime(PeriodEnum.DAY)
        if start is None:
            self._output.log('Nenhum registro a ser processado')
            return
        end = start + timedelta(days=self._days)

        next = True
        cycles = 0
        while next:
            cycles += 1
            self._output.log('Análisando ações de ' + Log.date(start) + ' até ' + Log.date(end))

            progress = 0
            length = len(stocks)
            part = 100 / length
            self._transaction.begin()
            try:
                for stock in stocks:

                    # obtem historico
                    historical = self._historic_service.get_historical(stock, start, end)
                    timelines = []
                    if len(historical) < period.value:
                        next = False
                        break
                    for historic in historical:
                        timelines.append(historic.timeline)

                    # realiza professias
                    self._prophet.set_historical(historical)
                    self._prophet.handle()
                    prophesies = self._prophet.results()
                    if len(prophesies) > 0:
                        analyze = AnalyzeEntity()
                        analyze.stock = stock
                        analyze.period = period
                        analyze.context = ContextEnum.TRAINING
                        analyze.timelines = timelines
                        analyze.save()
                        for prophesy in prophesies:
                            prophesy.analyze = analyze
                            prophesy.save()
                    self._prophet.flush()

                    # exibe percentual de processamento
                    progress += part
                    self._output.inline(Log.percentage(progress))
                self._output.log(' COMPLETO')
                self._transaction.commit()
            except Exception as error:
                self._transaction.rollback()
                raise error

            if self._rampant and self._cycles > cycles:
                end = end + timedelta(days=period.value)
                start = start + timedelta(days=period.value)
            else:
                next = False
        self._output.log('Fim da análise dos dados.')