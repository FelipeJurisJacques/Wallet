import gc
import pandas
from prophet import Prophet
from ..entities.historic import HistoricModel
from ..entities.prophesy import ProphesiedModel
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
        self._data = pandas.DataFrame(columns=[
            'ds',
            'y',
            'cap',
            'floor',
        ])
        for historic in historical:
            self._data.loc[len(self._data)] = [
                historic.date,
                historic.close,
                historic.high,
                historic.low,
            ]
        self._max = historical.pop().date
        self._close_forecast = []

    def handle(self, periods: int):
        self._prophet.fit(self._data)
        self._future = self._prophet.make_future_dataframe(periods=periods)
        self._close_forecast = self._prophet.predict(self._future)

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
    
    def flush(self):
        del self._max
        del self._data
        del self._future
        del self._prophet
        del self._close_forecast
        gc.collect()