from scipy.signal import find_peaks
from source.entities.forecast import Forecast as ForecastEntity
from source.entities.prophesy import Prophesy as ProphesyEntity
from source.enumerators.historic import Historic as HistoricEnum
from source.services.monetary.analyze import Analyze as AnalyzeService

# encapsulamento para manipular a profetizacao de valoes futuros de acoes de empresas e estimar ganhos
class Forecast:

    def __init__(self):
        self._service = AnalyzeService()
        
    def set_prophesies(
        self,
        open: list[ProphesyEntity],
        close: list[ProphesyEntity],
        volume: list[ProphesyEntity]
    ):
        self._open_prophesies = open
        self._close_prophesies = close
        self._volume_prophesies = volume

    def handle(self):
        self._open_forecasts = self._get_forecasts(self._open_prophesies)
        for forecast in self._open_forecasts:
            forecast.type = HistoricEnum.OPEN
        self._close_forecasts = self._get_forecasts(self._close_prophesies)
        for forecast in self._close_forecasts:
            forecast.type = HistoricEnum.CLOSE
        self._volume_forecasts = self._get_forecasts(self._volume_prophesies)
        for forecast in self._volume_forecasts:
            forecast.type = HistoricEnum.VOLUME

    def results(self) -> tuple[
        list[ForecastEntity], # OPEN
        list[ForecastEntity], # CLOSE
        list[ForecastEntity], # VOLUME
    ]:
        return self._open_forecasts, self._close_forecasts, self._volume_forecasts
    
    def flush(self):
        # del self._historical
        del self._open_forecasts
        del self._close_forecasts
        del self._volume_forecasts
        del self._open_prophesies
        del self._close_prophesies
        del self._volume_prophesies

    def _get_forecasts(self, data: list[ProphesyEntity]) -> list[ForecastEntity]:
        if len(data) == 0:
            return []
        result = []
        peaks = self._get_peaks(data, 1)
        for peak in peaks:
            forecast = self._generate_forecast(peak)
            if forecast is not None:
                result.append(forecast)
        return result

    def _generate_forecast(self, data: list[ProphesyEntity]) -> ForecastEntity:
        if len(data) < 2:
            return None
        last = data[-1]
        first = data[0]
        if last.timeline is None:
            raise ValueError('timeline is None')
        if first.timeline is None:
            raise ValueError('timeline is None')
        forecast = ForecastEntity()
        forecast.max_value = last.yhat
        forecast.min_value = first.yhat
        forecast.max_timeline = last.timeline
        forecast.min_timeline = first.timeline
        if forecast.min_timeline.datetime.timestamp() > forecast.max_timeline.datetime.timestamp():
            # evitar inversao
            return None
        if forecast.min_value > forecast.max_value:
            # evitar prejuiso
            return None
        forecast.type = first.type
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

    def _get_peaks(self, data: list[ProphesyEntity], multiply: int = 1) -> list[list[ProphesyEntity]]:
        if len(data) == 0:
            return []

        # processa valores
        values = []
        for prophesy in data:
            values.append(prophesy.yhat * multiply)
        peaks, _ = find_peaks(values)

        # organiza indices em grupos
        group = []
        index = 0
        groups = []
        for i in range(0, len(data)):
            group.append(i)
            if i == peaks[index]:
                groups.append(group)
                group = []
                if index < len(peaks) - 1:
                    index += 1
        if len(group) > 0:
            groups.append(group)

        # gera novos grupos maiores
        for i in range(0, len(groups) - 1):
            group = groups[i]
            groups.append(groups[i] + groups[i + 1])

        # transforma indices e entidades
        results = []
        for group in groups:
            result = []
            for index in group:
                result.append(data[index])
            result = self._ltrim(result)
            if len(result) > 1:
                results.append(result)

        return results
    
    def _trim(self, data: list[ProphesyEntity]) -> list[ProphesyEntity]:
        return self._rtrim(self._ltrim(data))

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