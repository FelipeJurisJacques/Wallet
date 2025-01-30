import gc
import pandas
import logging
from prophet import Prophet as Library
from source.enumerators.period import Period as PeriodEnum
from source.entities.historic import Historic as HistoricEntity
from source.entities.prophesy import Prophesy as ProphesyEntity
from source.enumerators.historic import Historic as HistoricEnum
from source.services.monetary.timeline import Timeline as TimelineService

# encapsulamento para manipular a biblioteca Prophet para prever valoes futuros de acoes de empresas
class Prophet:

    def __init__(self, type: HistoricEnum, input_period: PeriodEnum, output_period: PeriodEnum):
        # y: dados
        # ds: data
        # cap: limite superior
        # floor: limite inferior
        # holiday: datas de feriados ou eventos
        self._type = type
        self._input_period = input_period
        self._output_period = output_period
        self._timeline_service = TimelineService()
        
    def set_historical(self, historical: list[HistoricEntity]):
        self._historical = historical
        self._data = None
        self._forecast = None
        if self._type == HistoricEnum.VOLUME:
            self._data = pandas.DataFrame(columns=[
                'ds',
                'y',
            ])
        else:
            columns = [
                'ds',
                'y',
                'cap',
                'floor',
            ]
            # columns.append('v')
        self._data = pandas.DataFrame(columns=columns)
        i = 0
        for historic in historical:
            timeline = historic.timeline
            if self._type == HistoricEnum.VOLUME:
                self._data.loc[i] = [
                    timeline.datetime,
                    historic.volume,
                ]
            else:
                data = [
                    timeline.datetime,
                ]
                if self._type == HistoricEnum.OPEN:
                    data.append(historic.open)
                elif self._type == HistoricEnum.CLOSE:
                    data.append(historic.close)
                else:
                    raise Exception('Tipo de historico desconhecido')
                data.append(historic.high)
                data.append(historic.low)
                # data.append(historic.volume)
                self._data.loc[i] = data
            i += 1
        self._last = historical[i - 1]
        self._first = historical[0]
        timeline = self._last.timeline
        self._stock = timeline.stock

    def handle(self):
        if len(self._historical) == 0:
            return
        logging.getLogger('cmdstanpy').setLevel(logging.WARNING)
        logging.getLogger('prophet').setLevel(logging.WARNING)
        # model = Library(
        #     daily_seasonality=True,
        #     yearly_seasonality=False,
        #     weekly_seasonality=True,
        #     changepoint_prior_scale=0.01,
        #     seasonality_prior_scale=1.0,
        #     seasonality_mode='multiplicative',
        # )
        # self._volume_forecast = []
        # model.fit(self._volume_data)
        # future = model.make_future_dataframe(periods=self._output_period.value)
        # forecast = model.predict(future)
        # for row in forecast.to_dict('records'):
        #     self._volume_forecast.append(row['yhat'])
        self._forecast = self._get_forecast(self._data)
        logging.getLogger('cmdstanpy').setLevel(logging.INFO)
        logging.getLogger('prophet').setLevel(logging.INFO)

    def results(self) -> list[ProphesyEntity]:
        forecasts = self._persist(self._forecast)
        for forecast in forecasts:
            forecast.type = self._type
        return forecasts
    
    def flush(self):
        del self._last
        del self._data
        del self._first
        del self._stock
        del self._future
        del self._prophet
        del self._forecast
        del self._historical
        gc.collect()

    def _get_forecast(self, data):
        self._prophet = Library(
            daily_seasonality=True,
            yearly_seasonality=False,
            weekly_seasonality=True,
            changepoint_prior_scale=0.01,
            seasonality_prior_scale=1.0,
            seasonality_mode='multiplicative',
        )
        # self._prophet.add_regressor('v')
        self._prophet.fit(data)
        self._future = self._prophet.make_future_dataframe(periods=self._output_period.value)
        # self._future['v'] = self._volume_forecast
        return self._prophet.predict(self._future)
    
    def _persist(self, forecast) -> list[ProphesyEntity]:
        if forecast is None:
            return []
        end = self._last.timeline
        result = []
        for forecast in forecast.to_dict('records'):
            if end.datetime.timestamp() > forecast['ds'].timestamp():
                continue
            timeline = self._timeline_service.get_timeline(self._stock, self._input_period, forecast['ds'])
            if timeline is None:
                continue
            model = ProphesyEntity()
            model.timeline = timeline
            for key, value in forecast.items():
                if key != 'ds':
                    setattr(model, key, value)
            result.append(model)
        return result