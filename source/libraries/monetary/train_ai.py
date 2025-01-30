import numpy
from ..log import Log
from sklearn.linear_model import Ridge
from source.enumerators.period import Period as PeriodEnum
from source.enumerators.historic import Historic as HistoricEnum
from source.services.monetary.analyze import Analyze as AnalyzeService
from source.services.monetary.historic import Historic as HistoricService

class TrainAi:

    def __init__(self, log: Log):
        self._output = log
        self._analyze_service = AnalyzeService()
        self._historic_service = HistoricService()

    def handle(self):

        prophesies_values = []
        forecasts_max_values = []
        forecasts_min_values = []
        analyzes = self._analyze_service.get_all_to_train(PeriodEnum.MONTH)
        if len(analyzes) == 0:
            self._output.log('Nenhuma analise encontrada para treinamento.')
            return

        for analyze in analyzes:
            prophesies = self._analyze_service.get_prophesies(analyze, HistoricEnum.CLOSE)
            if len(prophesies) == 0:
                continue
            historical = self._historic_service.get_historical(
                analyze.stock,
                prophesies[0].timeline.datetime,
                prophesies[-1].timeline.datetime,
            )
            if len(historical) == 0:
                continue
            values = []
            for prophesy in prophesies:
                values.append(prophesy.yhat)
            prophesies_values.append(values)
            values = []
            for historic in historical:
                values.append(historic.close)
            historic = historical[0]
            forecasts_max_values.append(float(float(max(values) / historic.close) - 1.0))
            forecasts_min_values.append(float(float(min(values) / historic.close) - 1.0))

        if len(prophesies_values) == 0:
            self._output.log('Nenhuma profecia encontrada para treinamento.')
            return

        self._output.log('Iniciando treinamento...')
        x = numpy.array(prophesies_values)
        y = numpy.array(forecasts_max_values)
        z = numpy.array(forecasts_min_values)

        model = Ridge(alpha=0.01)
        model.fit(x, y)
        predicted_upper = model.predict(x)
        total = len(predicted_upper)

        model = Ridge(alpha=0.01)
        model.fit(x, z)
        predicted_lower = model.predict(x)

        fails = 0
        success = 0
        for i in range(total):
            compare = predicted_upper[i] + predicted_lower[i]
            if y[i] > 0.0 and compare > 0.0:
                success += 1
            elif y[i] < 0.0 and compare < 0.0:
                success += 1
            elif y[i] == 0.0 and compare == 0.0:
                success += 1
            else:
                fails += 1
            # self._output.log(f'Previsto {Log.percentage(predicted[i] * 100.0)} Real {Log.percentage(y[i] * 100.0)}')
        self._output.log(f'Acertos {success} Erros {fails} Total {total}')

    def flush(self):
        pass