import pandas
from prophet import Prophet
from ..models.historic import HistoricModel
from ..models.prophesied import ProphesiedModel
from ..enumerators.prophesied import ProphesiedEnum

class ProphetLib:

    def __init__(self):
        # y: dados
        # ds: data
        # cap: limite superior
        # floor: limite inferior
        # holiday: datas de feriados ou eventos
        pass
        
    def set_historical(self, historical: list[HistoricModel]):
        self._prophet = Prophet()
        data = pandas.DataFrame(columns=['ds', 'y'])
        for historic in historical:
            data.loc[len(data)] = [historic.date, historic.close]
        self._data = data
        self._max = historical.pop().date
        self._close_forecast = []

    def handle(self, periods: int):
        self._prophet.fit(self._data)
        future = self._prophet.make_future_dataframe(periods=periods)
        forecast = self._prophet.predict(future)
        self._prophet.plot(forecast)
        self._close_forecast = forecast

    def get_close_result(self) -> list[ProphesiedModel]:
        result = []
        for forecast in self._close_forecast.to_dict('records'):
            model = ProphesiedModel()
            model.type = ProphesiedEnum.CLOSE
            for key, value in forecast.items():
                if key == 'ds':
                    key = 'date'
                setattr(model, key, value)
            if model.date > self._max:
                result.append(model)
        return result