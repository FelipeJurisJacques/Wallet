import gc
import pandas
from prophet import Prophet
from ..enumerators.prophesied import ProphesiedEnum
from ..entities.historic_day import HistoricDayEntity
from ..entities.prophesy_day import ProphesyDayEntity

class ProphetLib:

    def __init__(self):
        # y: dados
        # ds: data
        # cap: limite superior
        # floor: limite inferior
        # holiday: datas de feriados ou eventos
        pass
        
    def set_historical(self, historical: list[HistoricDayEntity]):
        self._historical = historical
        self._open_data = pandas.DataFrame(columns=[
            'ds',
            'y',
            'cap',
            'floor',
        ])
        self._close_data = pandas.DataFrame(columns=[
            'ds',
            'y',
            'cap',
            'floor',
        ])
        self._volume_data = pandas.DataFrame(columns=[
            'ds',
            'y',
        ])
        i = 0
        for historic in historical:
            self._open_data.loc[i] = [
                historic.date,
                historic.open,
                historic.high,
                historic.low,
            ]
            self._close_data.loc[i] = [
                historic.date,
                historic.close,
                historic.high,
                historic.low,
            ]
            self._volume_data.loc[i] = [
                historic.date,
                historic.volume,
            ]
            i += 1
        self._max = historical.pop().date
        self._open_forecast = []
        self._close_forecast = []
        self._volume_forecast = []

    def handle(self, periods: int):
        self._open_forecast = self._get_forecast(self._open_data, periods)
        self._close_forecast = self._get_forecast(self._close_data, periods)
        self._volume_forecast = self._get_forecast(self._volume_data, periods)

    def get_open_result(self) -> list[ProphesyDayEntity]:
        return self._get_result(self._open_forecast, ProphesiedEnum.OPEN)

    def get_close_result(self) -> list[ProphesyDayEntity]:
        return self._get_result(self._close_forecast, ProphesiedEnum.CLOSE)

    def get_volume_result(self) -> list[ProphesyDayEntity]:
        return self._get_result(self._volume_forecast, ProphesiedEnum.VOLUME)
    
    def flush(self):
        del self._max
        del self._future
        del self._prophet
        del self._open_data
        del self._close_data
        del self._historical
        del self._volume_data
        del self._open_forecast
        del self._close_forecast
        del self._volume_forecast
        gc.collect()

    def _get_forecast(self, data, periods):
        self._prophet = Prophet()
        self._prophet.fit(data)
        self._future = self._prophet.make_future_dataframe(periods=periods)
        return self._prophet.predict(self._future)
    
    def _get_result(self, forecast, type):
        day = 0
        end = self._historical[len(self._historical) - 1]
        start = self._historical[0]
        result = []
        for forecast in forecast.to_dict('records'):
            model = ProphesyDayEntity()
            for key, value in forecast.items():
                if key == 'ds':
                    key = 'date'
                setattr(model, key, value)
            if model.date > self._max:
                day += 1
                model.type = type
                model.data_end_date = end.date
                model.increased_day = day
                model.data_start_date = start.date
                model.last_historic = end
                result.append(model)
        del day
        del end
        del start
        return result