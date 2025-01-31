from ..log import Log
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
        self._days = 100
        self._cycles = 10
        self._output = log
        self._timeline_service = TimelineService()
        self._historic_service = HistoricService()

    def handle(self):

        # obtem empresas
        stocks = StockEntity.all()
        if len(stocks) == 0:
            self._output.log('Nenhuma empresa cadastrada')
            return
        # stocks = stocks[:2]

        start = self._timeline_service.get_min_datetime(PeriodEnum.DAY)
        if start is None:
            self._output.log('Nenhum registro a ser processado')
            return
        end = start + timedelta(days=self._days)

        cycles = 0
        transaction = Transaction()
        delta = timedelta(days=PeriodEnum.MONTH.value)
        while self._cycles > cycles:
            cycles += 1
            self._output.log('Análisando ações de ' + Log.date(start) + ' até ' + Log.date(end))

            progress = 0
            length = len(stocks)
            part = 100 / length
            transaction.begin()
            try:
                for stock in stocks:

                    # obtem historico
                    historical = self._historic_service.get_historical(stock, start, end)
                    timelines = []
                    if len(historical) < PeriodEnum.MONTH.value:
                        break
                    for historic in historical:
                        timelines.append(historic.timeline)

                    # realiza professias
                    prophet = Prophet(
                        type=HistoricEnum.CLOSE,
                        input_period=PeriodEnum.DAY,
                        output_period=PeriodEnum.MONTH
                    )
                    prophet.set_historical(historical)
                    prophet.handle()
                    prophesies = prophet.results()
                    if len(prophesies) > 0:
                        analyze = AnalyzeEntity()
                        analyze.stock = stock
                        analyze.period = PeriodEnum.MONTH
                        analyze.context = ContextEnum.TRAINING
                        analyze.timelines = timelines
                        analyze.save()
                        for prophesy in prophesies:
                            prophesy.analyze = analyze
                            prophesy.save()
                    prophet.flush()

                    # exibe percentual de processamento
                    progress += part
                    self._output.inline(Log.percentage(progress))

                self._output.log(' COMPLETO')
                transaction.commit()
            except Exception as error:
                transaction.rollback()
                raise error

            end = end + delta
            start = start + delta

        self._output.log('Fim da análise dos dados.')