import gc
import pandas
from prophet import Prophet
from datetime import datetime
from scipy.signal import find_peaks
from ..entities.period import PeriodEntity
from ..enumerators.period import PeriodEnum
from ..services.analyze import AnalyzeService
from ..entities.forecast import ForecastEntity
from ..entities.historic import HistoricEntity
from ..entities.prophesy import ProphesyEntity
from ..enumerators.historic import HistoricEnum
from ..libraries.database.transaction import TransactionLib

# encapsulamento para manipular a profetizacao de valoes futuros de acoes de empresas e estimar ganhos
class ForecastLib:

    def __init__(self):
        self._service = AnalyzeService()
        self._transaction = TransactionLib()
        
    def set_prophesies(self, prophesies: list[ProphesyEntity]):
        self._open_prophesies = []
        self._close_prophesies = []
        if len(prophesies) > 0:
            self._period = prophesies[0].period
            for prophesy in prophesies:
                if prophesy.type == HistoricEnum.OPEN:
                    self._open_prophesies.append(prophesy)
                if prophesy.type == HistoricEnum.CLOSE:
                    self._close_prophesies.append(prophesy)

    def set_historical(self, historical: list[HistoricEntity]):
        self._historical = historical
        self._open_prophesies = self._historical_compare(self._open_prophesies)
        self._close_prophesies = self._historical_compare(self._close_prophesies)

    def handle(self):
        self._open_forecast = self._get_forecast(self._open_prophesies)
        self._close_forecast = self._get_forecast(self._close_prophesies)

    def persist(self):
        # print('valores')
        # for prophesy in self._close_prophesies:
            # print(prophesy.yhat)
        todos = 0
        lucrados = 0
        perdidos = 0
        for forecast in self._close_forecast:
            todos += 1
            print('parte')
            print(forecast.forecast_min_value)
            # print(forecast.corrected_min_value)
            print(forecast.forecast_max_value)
            # print(forecast.corrected_max_value)
            # print(forecast.forecast_min_value)
            # print(forecast.forecast_max_value)
            # print(forecast.forecast_difference)
            # print(forecast.forecast_percentage)
            # print(forecast.corrected_percentage)
            if forecast.corrected_percentage is not None:
                if forecast.forecast_percentage > 0:
                    if forecast.corrected_percentage > 0:
                        lucrados += 1
                    else:
                        perdidos += 1
        return todos, lucrados, perdidos

        # self._transaction.start()
        # try:
        #     self._transaction.commit()
        # except Exception as error:
        #     self._transaction.rollback()
        #     raise error
    
    def flush(self):
        del self._open_forecast
        del self._close_forecast
        del self._open_prophesies
        del self._close_prophesies

    def _get_forecast(self, data: list[ProphesyEntity]) -> list[ForecastEntity]:
        length = len(data)
        if length == 0:
            return []
        result = []
        print(length)
        data = self._trim(data)
        length = len(data)
        print(length)
        if length > 0:
            # maxs = self._get_peaks(data, 1)
            # mins = self._get_peaks(data, -1)
            # intervals = self._get_intervals(mins, maxs)
            # for interval in intervals:
            #     end = interval[-1]
            #     start = interval[0]
            #     forecast = self._generate_forecast(data[start:end])
            #     if forecast is not None:
            #         result.append(forecast)
            forecast = self._generate_forecast(data)
            if forecast is not None:
                result.append(forecast)
        return result
    
    def _trim(self, data: list[ProphesyEntity]) -> list[ProphesyEntity]:
        return self._rtrim(self._ltrim(data))
        # return self._rtrim(data)

    def _ltrim(self, data: list[ProphesyEntity]) -> list[ProphesyEntity]:
        length = len(data)
        if length > 1:
            if data[0].yhat > data[1].yhat:
                return self._ltrim(data[1:length])
        return data

    def _rtrim(self, data: list[ProphesyEntity]) -> list[ProphesyEntity]:
        length = len(data)
        if length > 1:
            if data[-2].yhat > data[-1].yhat:
                length -= 1
                return self._rtrim(data[0:length])
        return data

    def _get_intervals(self, mins, maxs) -> list:
        last = None
        result = []
        for max in maxs:
            end = max
            start = 0
            for min in mins:
                if max > min:
                    start = min
            if last == start:
                result[len(result) - 1] = [
                    start,
                    end,
                ]
            else:
                result.append([
                    start,
                    end,
                ])
                last = start
        return result

    def _get_peaks(self, data: list[ProphesyEntity], multiply: int = 1):
        result = []
        if len(data) > 0:
            if multiply < 0:
                result.append(0)
            values = []
            for prophesy in data:
                values.append(prophesy.yhat * multiply)
            peaks, _ = find_peaks(values)
            for peak in peaks:
                result.append(peak)
            if multiply > 0:
                result.append(len(values) - 1)
        return result

    def _generate_forecast(self, data: list[ProphesyEntity]) -> ForecastEntity:
        if len(data) < 3:
            # avaliar periodo superior de 2 dias
            return None
        min_date = None
        max_date = None
        min_value = None
        max_value = None
        for prophesy in data:
            if min_value is None or prophesy.yhat < min_value:
                min_date = prophesy.date
                min_value = prophesy.yhat
            if max_value is None or prophesy.yhat > max_value:
                max_date = prophesy.date
                max_value = prophesy.yhat
        if min_date >= max_date:
            # evitar inversao
            return None
        if min_value > max_value:
            # evitar prejuiso
            return None
        forecast = ForecastEntity()
        forecast.period = self._period
        forecast.historical = data[0].type
        forecast.forecast_min_value = min_value
        forecast.forecast_max_value = max_value
        forecast.forecast_min_moment = min_date
        forecast.forecast_max_moment = max_date
        forecast.forecast_difference = forecast.forecast_max_value - forecast.forecast_min_value
        forecast.forecast_percentage = 100 * (forecast.forecast_max_value / forecast.forecast_min_value - 1)
        min = self._get_historic(min_date)
        max = self._get_historic(max_date)
        if min is not None and max is not None:
            forecast.corrected_min_value = min.close
            forecast.corrected_max_value = max.close
            forecast.corrected_min_moment = min.date
            forecast.corrected_max_moment = max.date
            forecast.corrected_difference = max.close - min.close
            forecast.corrected_percentage = 100 * (max.close / min.close - 1)
        return forecast

    def _historical_compare(self, prophesies: list[ProphesyEntity]):
        if len(prophesies) == 0:
            return []
        length = len(self._historical)
        if length == 0:
            return prophesies
        result = []
        for prophesy in prophesies:
            i = 0
            time = prophesy.date.timestamp()
            end = time + 43200
            start = time - 43200
            contains = False
            for historic in self._historical:
                i += 1
                time = historic.date.timestamp()
                if (time > start and time < end) or (i == length and end > time):
                    contains = True
                    break
            if contains == True:
                result.append(prophesy)
        return result

    def _get_historic(self, date: datetime):
        time = date.timestamp()
        end = time + 43200
        start = time - 43200
        for historic in self._historical:
            time = historic.date.timestamp()
            if time > start and time < end:
                return historic
        return None
    
    def _persist(self, forecast) -> list[ProphesyEntity]:
        if forecast is None:
            return []
        day = 0
        end = self._last
        start = self._first
        result = []
        for forecast in forecast.to_dict('records'):
            if end.date.timestamp() > forecast['ds'].timestamp():
                continue
            model = ProphesyEntity()
            for key, value in forecast.items():
                if key == 'ds':
                    key = 'date'
                setattr(model, key, value)
            if model.date > self._last.date:
                day += 1
                model.increased = day
                model.data_end_date = end.date
                model.data_start_date = start.date
                result.append(model)
        del day
        del end
        del start
        return result