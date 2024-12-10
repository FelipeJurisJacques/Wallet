import gc
import pandas
from prophet import Prophet
from ..entities.period import PeriodEntity
from ..enumerators.period import PeriodEnum
from ..entities.historic import HistoricEntity
from ..entities.prophesy import ProphesyEntity
from ..enumerators.historic import HistoricEnum
from ..libraries.database.transaction import TransactionLib

class ProphetLib:

    def __init__(self):
        # y: dados
        # ds: data
        # cap: limite superior
        # floor: limite inferior
        # holiday: datas de feriados ou eventos
        self._transaction = TransactionLib()
        
    def set_historical(self, historical: list[HistoricEntity]):
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
            i += 1
        self._last = historical[i - 1]
        self._first = historical[0]
        self._open_forecast = []
        self._close_forecast = []

    def handle(self, period: PeriodEnum):
        self._period = period
        self._open_forecast = self._get_forecast(self._open_data, period)
        self._close_forecast = self._get_forecast(self._close_data, period)

    def persist(self):
        self._transaction.start()
        try:
            end = self._last
            opens = self._persist(self._open_forecast)
            closes = self._persist(self._close_forecast)
            period = PeriodEntity()
            period.period = self._period
            period.historical = self._historical
            period.save()
            for open in opens:
                open.type = HistoricEnum.OPEN
                open.period = period
                open.save()
                del open
            for close in closes:
                close.type = HistoricEnum.CLOSE
                close.period = period
                close.save()
                del close
            self._transaction.commit()
            del end
            del opens
            del closes
        except Exception as error:
            self._transaction.rollback()
            raise error
    
    def flush(self):
        del self._last
        del self._first
        del self._future
        del self._prophet
        del self._open_data
        del self._close_data
        del self._historical
        del self._open_forecast
        del self._close_forecast
        gc.collect()

    def _get_forecast(self, data, period: PeriodEnum):
        self._prophet = Prophet(
            daily_seasonality=True,
            yearly_seasonality=True,
            weekly_seasonality=True,
            changepoint_prior_scale=0.05,
            seasonality_prior_scale=10,
            # seasonality_mode='multiplicative',
        )
        self._prophet.fit(data)
        self._future = self._prophet.make_future_dataframe(periods=period.value)
        return self._prophet.predict(self._future)
    
    def _persist(self, forecast) -> list[ProphesyEntity]:
        day = 0
        end = self._last
        start = self._first
        result = []
        for forecast in forecast.to_dict('records'):
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