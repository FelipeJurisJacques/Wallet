import numpy
import joblib
from django.conf import settings
from source.entities.forecast import Forecast as ForecastEntity
from source.entities.prophesy import Prophesy as ProphesyEntity
from source.enumerators.historic import Historic as HistoricEnum
from source.services.monetary.analyze import Analyze as AnalyzeService

# encapsulamento para manipular a profetizacao de valoes futuros de acoes de empresas e estimar ganhos
class Forecast:

    def __init__(self):
        self._service = AnalyzeService()
        self._open_prophesies = []
        self._close_prophesies = []
        self._volume_prophesies = []
        self._close_quantitative_model = joblib.load(
            settings.AI_MODELS_DIR / 'ridge_model_prophesy_close_month_quantitative.joblib'
        )
        
    def set_close_prophesies(self, prophesies: list[ProphesyEntity]):
        self._close_prophesies = prophesies

    def handle(self):
        self._open_forecast = []
        self._close_forecasts = []
        forecast = self._get_forecast(self._open_prophesies)
        if forecast is not None:
            forecast.type = HistoricEnum.OPEN
            self._open_forecast.append(forecast)
        forecast = self._get_forecast(self._close_prophesies)
        if forecast is not None:
            forecast.type = HistoricEnum.CLOSE
            self._close_forecasts.append(forecast)

    def results(self) -> tuple[
        list[ForecastEntity], # OPEN
        list[ForecastEntity], # CLOSE
    ]:
        return self._open_forecast, self._close_forecasts
    
    def flush(self):
        self._open_prophesies = []
        self._close_prophesies = []
        self._volume_prophesies = []
        del self._open_forecast
        del self._close_forecasts

    def _get_forecast(self, data: list[ProphesyEntity]) -> ForecastEntity:
        if len(data) == 0:
            return None
        values = []
        for prophesy in data:
            values.append(prophesy.yhat)
        x = numpy.array([
            values,
        ])
        quantitative = self._close_quantitative_model.predict(x)[0]
        if quantitative < 0.0:
            return None
        entity = ForecastEntity()
        entity.min_value = data[0].yhat
        entity.max_value = data[-1].yhat
        entity.min_timeline = data[0].timeline
        entity.max_timeline = data[-1].timeline
        entity.percentage = quantitative
        entity.difference = entity.max_value - entity.min_value
        entity.quantitative = quantitative
        entity.interval = int(
            entity.max_timeline.datetime.timestamp() - entity.min_timeline.datetime.timestamp()
        )
        return entity