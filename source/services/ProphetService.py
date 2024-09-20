import pandas
from prophet import Prophet
from ..model.HistoricModel import HistoricModel
from ..model.ProphesiedModel import ProphesiedModel

class ProphetService(Prophet):
    def __init__(self, historical: list[HistoricModel]):
        super().__init__()
        # y: dados
        # ds: data
        # cap: limite superior
        # floor: limite inferior
        # holiday: datas de feriados ou eventos
        data = pandas.DataFrame(columns=['ds', 'y'])
        for historic in historical:
            data.loc[len(data)] = [historic.date, historic.close]
        self._data = data
        self._max = historical.pop().date

    def handle(self, periods: int):
        super().fit(self._data)
        future = super().make_future_dataframe(periods=periods)
        forecast = super().predict(future)
        super().plot(forecast)
        self._forecast = forecast

    def result(self) -> list[ProphesiedModel]:
        result = []
        for forecast in self._forecast.to_dict('records'):
            # result.append(ProphesiedModel(Entity(**dict(forecast))))
            model = ProphesiedModel()
            for key, value in forecast.items():
                match key:
                    case 'ds':
                        model.date = value
                    case 'trend':
                        model.trend = value
                    case 'yhat_lower':
                        model.yhatLower = value
                    case 'yhat_upper':
                        model.yhatUpper = value
                    case 'trend_lower':
                        model.trendLower = value
                    case 'trend_upper':
                        model.trendUpper = value
                    case 'additive_terms':
                        model.additiveTerms = value
                    case 'additive_terms_lower':
                        model.additiveTermsLower = value
                    case 'additive_terms_upper':
                        model.additiveTermsUpper = value
                    case 'weekly':
                        model.weekly = value
                    case 'weekly_lower':
                        model.weeklyLower = value
                    case 'weekly_upper':
                        model.weeklyUpper = value
                    case 'yearly':
                        model.yearly = value
                    case 'yearly_lower':
                        model.yearlyLower = value
                    case 'yearly_upper':
                        model.yearlyUpper = value
                    case 'multiplicative_terms':
                        model.multiplicativeTerms = value
                    case 'multiplicative_terms_lower':
                        model.multiplicativeTermsLower = value
                    case 'multiplicative_terms_upper':
                        model.multiplicativeTermsUpper = value
                    case 'yhat':
                        model.yhat = value
            if model.date > self._max:
                result.append(model)
        return result