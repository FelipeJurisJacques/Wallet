from datetime import datetime
from scipy.signal import find_peaks
from source.libraries.database.transaction import Transaction
from source.entities.forecast import Forecast as ForecastEntity
from source.entities.historic import Historic as HistoricEntity
from source.entities.prophesy import Prophesy as ProphesyEntity
from source.enumerators.historic import Historic as HistoricEnum
from source.services.monetary.analyze import Analyze as AnalyzeService

# encapsulamento para manipular a profetizacao de valoes futuros de acoes de empresas e estimar ganhos
class Forecast:

    def __init__(self):
        self._service = AnalyzeService()
        self._transaction = Transaction()
        
    def set_prophesies(
        self,
        open: list[ProphesyEntity],
        close: list[ProphesyEntity],
        volume: list[ProphesyEntity]
    ):
        self._open_prophesies = open
        self._close_prophesies = close
        self._volume_prophesies = volume

    # def set_historical(self, historical: list[HistoricEntity]):
    #     self._historical = historical
    #     self._open_prophesies = self._historical_compare(self._open_prophesies)
    #     self._close_prophesies = self._historical_compare(self._close_prophesies)

    def handle(self):
        self._open_forecast = self._get_forecast(self._open_prophesies)
        for forecast in self._open_forecast:
            forecast.type = HistoricEnum.OPEN
        self._close_forecast = self._get_forecast(self._close_prophesies)
        for forecast in self._close_forecast:
            forecast.type = HistoricEnum.CLOSE
        self._volume_forecast = self._get_forecast(self._volume_prophesies)
        for forecast in self._volume_forecast:
            forecast.type = HistoricEnum.VOLUME

    def results(self) -> tuple[
        list[ForecastEntity], # OPEN
        list[ForecastEntity], # CLOSE
        list[ForecastEntity], # VOLUME
    ]:
        return self._open_forecast, self._close_forecast, self._volume_forecast

    def persist(self):
        self._transaction.start()
        try:
            for prophesy in self._close_forecast:
                prophesy.save()
            for forecast in self._close_forecast:
                forecast.save()
            self._transaction.commit()
        except Exception as error:
            self._transaction.rollback()
            raise error
    
    def flush(self):
        # del self._historical
        del self._open_forecast
        del self._close_forecast
        del self._volume_forecast
        del self._open_prophesies
        del self._close_prophesies
        del self._volume_prophesies

    def _get_forecast(self, data: list[ProphesyEntity]) -> list[ForecastEntity]:
        length = len(data)
        if length == 0:
            return []
        result = []
        data = self._trim(data)
        length = len(data)
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
        min = None
        max = None
        min_value = None
        max_value = None
        length = len(data)
        for i in range(length):
            prophesy = data[i]
            if min_value is None or prophesy.yhat < min_value:
                if i > 1:
                    min = i - 2
                else:
                    min = i
                min_value = prophesy.yhat
            if max_value is None or prophesy.yhat > max_value:
                if (i + 2) >= length:
                    max = i
                else:
                    max = i + 2
                max_value = prophesy.yhat
        end = data[max]
        start = data[min]
        forecast = ForecastEntity()
        forecast.max_value = end.yhat
        forecast.min_value = start.yhat
        forecast.max_timeline = end.timeline
        forecast.min_timeline = start.timeline
        if forecast.min_timeline.datetime.timestamp() > forecast.max_timeline.datetime.timestamp():
            # evitar inversao
            return None
        if forecast.min_value > forecast.max_value:
            # evitar prejuiso
            return None
        forecast.type = start.type
        forecast.interval = int(
            forecast.max_timeline.datetime.timestamp() - forecast.min_timeline.datetime.timestamp()
        )
        forecast.difference = forecast.max_value - forecast.min_value
        forecast.percentage = 100 * (forecast.max_value / forecast.min_value - 1)
        forecast.quantitative = (
            forecast.percentage / forecast.interval
        ) * 10000000
        if forecast.percentage > 0.0:
            return forecast
        else:
            return None

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