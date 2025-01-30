import numpy
from ..log import Log
from .analyze import Analyze
from .prophet import Prophet
from datetime import timedelta
from sklearn.linear_model import Ridge
from source.entities.stock import Stock as StockEntity
from source.enumerators.period import Period as PeriodEnum
from source.entities.prophesy import Prophesy as ProphesyEntity
from source.enumerators.historic import Historic as HistoricEnum
from source.services.monetary.historic import Historic as HistoricService
from source.services.monetary.timeline import Timeline as TimelineService

class Train:

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
        self._timeline_service = TimelineService()
        self._historic_service = HistoricService()
        self._prophet = Prophet([
            HistoricEnum.CLOSE
        ], PeriodEnum.DAY)

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
        end = start + timedelta(days=self._days + period.value)

        next = True
        open_prophesies_values = []
        open_min_prophesies_values = []
        open_max_prophesies_values = []
        close_prophesies_values = []
        close_min_prophesies_values = []
        close_max_prophesies_values = []
        volume_prophesies_values = []
        volume_min_prophesies_values = []
        volume_max_prophesies_values = []
        open_forecasts_values = []
        close_forecasts_values = []
        volume_forecasts_values = []

        cycles = 0
        while next:
            cycles += 1
            self._output.log('Análisando ações de ' + Log.date(start) + ' até ' + Log.date(end))

            progress = 0
            length = len(stocks)
            part = 100 / length
            for stock in stocks:

                # obtem historico
                historical = self._historic_service.get_historical(stock, start, end)
                if len(historical) < period.value:
                    next = False
                    break

                # separa historico para analisar e treinar
                forecast_entities = []
                historic_entities = []
                cut = end - timedelta(days=period.value)
                for historic in historical:
                    if historic.timeline.datetime > cut:
                        forecast_entities.append(historic)
                    else:
                        historic_entities.append(historic)

                # realiza professias
                self._prophet.set_historical(historic_entities)
                self._prophet.handle()
                open_prophesies, close_prophesies, volume_prophesies = self._prophet.results()

                # extrai dados para treinamento
                if len(open_prophesies) > 0:
                    values, max_values, min_values = self._get_prophesy_values(open_prophesies)
                    open_prophesies_values.append(values)
                    open_min_prophesies_values.append(min_values)
                    open_max_prophesies_values.append(max_values)
                    open_value = None
                    for i in range(len(historic_entities)):
                        if 3 > i:
                            continue
                        historic = historic_entities[i]
                        if open_value is None or historic.open > open_value:
                            open_value = historic.open
                    historic = forecast_entities[0]
                    open_forecasts_values.append(float(float(open_value / historic.open) - 1.0))
                if len(close_prophesies) > 0:
                    values, max_values, min_values = self._get_prophesy_values(close_prophesies)
                    close_prophesies_values.append(values)
                    close_min_prophesies_values.append(min_values)
                    close_max_prophesies_values.append(max_values)
                    close_value = None
                    for i in range(len(historic_entities)):
                        if 3 > i:
                            continue
                        historic = historic_entities[i]
                        if close_value is None or historic.close > close_value:
                            close_value = historic.close
                    historic = forecast_entities[0]
                    close_forecasts_values.append(float(float(close_value / historic.close) - 1.0))
                if len(volume_prophesies) > 0:
                    values, max_values, min_values = self._get_prophesy_values(volume_prophesies)
                    volume_prophesies_values.append(values)
                    volume_min_prophesies_values.append(min_values)
                    volume_max_prophesies_values.append(max_values)
                    volume_value = None
                    for i in range(len(historic_entities)):
                        if 3 > i:
                            continue
                        historic = historic_entities[i]
                        if volume_value is None or historic.volume > volume_value:
                            volume_value = historic.volume
                    historic = forecast_entities[0]
                    volume_forecasts_values.append(float(float(volume_value / historic.volume) - 1.0))

                self._prophet.flush()
                progress += part
                self._output.inline(Log.percentage(progress))
            self._output.log(' COMPLETO')

            if self._rampant and self._cycles > cycles:
                end = end + timedelta(days=period.value)
                start = start + timedelta(days=period.value)
            else:
                next = False
        self._output.log('Fim da análise dos dados. Iniciando treinamento...')

        # treina
        if len(close_prophesies_values) > 0:
            model = Ridge(alpha=0.01)
            x = numpy.array(close_prophesies_values)
            y = numpy.array(close_forecasts_values)
            model.fit(x, y)
            predicted = model.predict(x)
            total = len(predicted)
            fails = 0
            success = 0
            for i in range(len(predicted)):
                if y[i] > 0 and predicted[i] < 0:
                    fails += 1
                elif y[i] < 0 and predicted[i] > 0:
                    fails += 1
                else:
                    success += 1
                self._output.log(f'Previsto {Log.percentage(predicted[i] * 100.0)} Real {Log.percentage(y[i] * 100.0)}')
            self._output.log(f'Acertos {success} Erros {fails} Total {total}')
        del open_prophesies_values
    
    def flush(self):
        pass

    def _get_prophesy_values(self, data: list[ProphesyEntity]):
        values = []
        max_values = []
        min_values = []
        for prophesy in data:
            values.append(prophesy.yhat)
            max_values.append(prophesy.yhat_upper)
            min_values.append(prophesy.yhat_lower)
        return values, max_values, min_values