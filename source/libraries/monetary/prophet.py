import gc
import pandas
from prophet import Prophet as Library
from source.enumerators.period import Period as PeriodEnum
from source.entities.historic import Historic as HistoricEntity
from source.entities.prophesy import Prophesy as ProphesyEntity
from source.enumerators.historic import Historic as HistoricEnum
from source.services.monetary.timeline import Timeline as TimelineService

# encapsulamento para manipular a biblioteca Prophet para prever valoes futuros de acoes de empresas
class Prophet:

    def __init__(self, results: list[HistoricEnum], period: PeriodEnum):
        # y: dados
        # ds: data
        # cap: limite superior
        # floor: limite inferior
        # holiday: datas de feriados ou eventos
        self._period = period
        self._is_volume = False
        if len(results) == 0:
            self._is_open = True
            self._is_close = True
        else:
            self._is_open = False
            self._is_close = False
            for result in results:
                if result == HistoricEnum.OPEN:
                    self._is_open = True
                elif result == HistoricEnum.CLOSE:
                    self._is_close = True
        self._timeline_service = TimelineService()
        
    def set_historical(self, historical: list[HistoricEntity]):
        self._historical = historical
        self._open_data = None
        self._close_data = None
        self._volume_data = None
        self._open_forecast = None
        self._close_forecast = None
        self._volume_forecast = None
        columns = [
            'ds',
            'y',
            'cap',
            'floor',
        ]
        if self._is_volume:
            columns.append('v')
        if self._is_open:
            self._open_data = pandas.DataFrame(columns=columns)
        if self._is_close:
            self._close_data = pandas.DataFrame(columns=columns)
        if self._is_volume:
            self._volume_data = pandas.DataFrame(columns=[
                'ds',
                'y',
            ])
        i = 0
        for historic in historical:
            timeline = historic.timeline
            if self._is_open:
                data = [
                    timeline.datetime,
                    historic.open,
                    historic.high,
                    historic.low,
                ]
                if self._is_volume:
                    data.append(historic.volume)
                self._open_data.loc[i] = data
            if self._is_close:
                data = [
                    timeline.datetime,
                    historic.close,
                    historic.high,
                    historic.low,
                ]
                if self._is_volume:
                    data.append(historic.volume)
                self._close_data.loc[i] = data
            if self._is_volume:
                self._volume_data.loc[i] = [
                    timeline.datetime,
                    historic.volume,
                ]
            i += 1
        self._last = historical[i - 1]
        self._first = historical[0]
        timeline = self._last.timeline
        self._type = timeline.type
        self._stock = timeline.stock

    def handle(self):
        if len(self._historical) == 0:
            return
        if self._is_volume:
            model = Library(
                daily_seasonality=True,
                yearly_seasonality=False,
                weekly_seasonality=True,
                changepoint_prior_scale=0.01,
                seasonality_prior_scale=1.0,
                seasonality_mode='multiplicative',
            )
            self._volume_forecast = []
            model.fit(self._volume_data)
            future = model.make_future_dataframe(periods=self._period.value)
            forecast = model.predict(future)
            for row in forecast.to_dict('records'):
                self._volume_forecast.append(row['yhat'])
        if self._is_open:
            self._open_forecast = self._get_forecast(self._open_data)
        if self._is_close:
            self._close_forecast = self._get_forecast(self._close_data)

    def results(self) -> tuple[
        list[ProphesyEntity], # OPEN
        list[ProphesyEntity], # CLOSE
        list[ProphesyEntity], # VOLUME
    ]:
        opens = self._persist(self._open_forecast)
        for open in opens:
            open.type = HistoricEnum.OPEN
        closes = self._persist(self._close_forecast)
        for close in closes:
            close.type = HistoricEnum.CLOSE
        return opens, closes, []
    
    def flush(self):
        del self._last
        del self._type
        del self._first
        del self._stock
        del self._future
        del self._prophet
        del self._open_data
        del self._close_data
        del self._historical
        del self._volume_data
        del self._open_forecast
        del self._close_forecast
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
        if self._is_volume:
            self._prophet.add_regressor('v')
        self._prophet.fit(data)
        self._future = self._prophet.make_future_dataframe(periods=self._period.value)
        if self._is_volume:
            self._future['v'] = self._volume_forecast
        return self._prophet.predict(self._future)
    
    def _persist(self, forecast) -> list[ProphesyEntity]:
        if forecast is None:
            return []
        end = self._last.timeline
        result = []
        for forecast in forecast.to_dict('records'):
            if end.datetime.timestamp() > forecast['ds'].timestamp():
                continue
            timeline = self._timeline_service.get_timeline(self._stock, self._type, forecast['ds'])
            if timeline is None:
                continue
            model = ProphesyEntity()
            model.timeline = timeline
            for key, value in forecast.items():
                if key != 'ds':
                    setattr(model, key, value)
            result.append(model)
        return result