import numpy
import joblib
from ..log import Log
from django.conf import settings
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
        forecasts_quantitative = []
        analyzes = self._analyze_service.get_all_to_train(PeriodEnum.MONTH)
        total = len(analyzes)
        if total == 0:
            self._output.log('Nenhuma analise encontrada para treinamento.')
            return

        index = 0
        self._output.log(f'Analisando {total} professias...')
        for analyze in analyzes:
            index += 1
            percent = int((index / total) * 100)
            if total > 1000 and index % 100 != 0:
                continue
            self._output.inline(f'{percent}%')
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
            length = len(values)
            min_value = min(values)
            max_value = max(values)
            # min_position = values.index(min_value)
            max_position = values.index(max_value)
            start_value = historical[0].close
            intensity = float(length - max_position) / float(length)
            upper = (float(max_value) / float(start_value)) - 1.0
            upper *= intensity
            lower = (float(min_value) / float(start_value)) - 1.0
            lower *= intensity
            forecasts_quantitative.append((upper + lower) * 100.0)

        if len(prophesies_values) == 0:
            self._output.log('Nenhuma profecia encontrada para treinamento.')
            return

        self._output.log('Iniciando treinamento...')
        x = numpy.array(prophesies_values)

        model = Ridge(alpha=0.01)
        model.fit(x, numpy.array(forecasts_quantitative))
        joblib.dump(
            model,
            settings.AI_MODELS_DIR / 'ridge_model_prophesy_close_month_quantitative.joblib'
        )
        predicted_quantitative = model.predict(x)
        total = len(predicted_quantitative)

        # model = Ridge(alpha=0.01)
        # model.fit(x, numpy.array(forecasts_end_values))
        # joblib.dump(
        #     model,
        #     settings.AI_MODELS_DIR / 'ridge_model_prophesy_close_month_end.joblib'
        # )

        # model = Ridge(alpha=0.01)
        # model.fit(x, numpy.array(forecasts_start_values))
        # joblib.dump(
        #     model,
        #     settings.AI_MODELS_DIR / 'ridge_model_prophesy_close_month_start.joblib'
        # )

        # fails = 0
        # success = 0
        # for i in range(total):
        #     if forecasts_values[i] > 0.0 and predicted_quantitative[i] > 0.0:
        #         success += 1
        #     elif forecasts_values[i] < 0.0 and predicted_quantitative[i] < 0.0:
        #         success += 1
        #     elif forecasts_values[i] == 0.0 and predicted_quantitative[i] == 0.0:
        #         success += 1
        #     else:
        #         fails += 1
        #     forecast = Log.percentage(predicted_quantitative[i] * 100.0)
        #     historic = Log.percentage(forecasts_values[i] * 100.0)
        #     lower = forecasts_start_values[i]
        #     upper = forecasts_end_values[i]
        #     self._output.log(f'Previsto {forecast} Real {historic} Deslocamento menor {lower} Deslocamento maior {upper}')
        # self._output.log(f'Acertos {success} Erros {fails} Total {total}')

        print(f'{total = } {forecasts_quantitative = } {predicted_quantitative = }')

        self._output.log('Treinamento concluido.')

    def flush(self):
        pass