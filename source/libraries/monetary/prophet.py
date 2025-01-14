import gc
import pandas
from datetime import datetime
from prophet import Prophet as Library
from source.entities.period import Period as PeriodEntity
from source.enumerators.period import Period as PeriodEnum
from source.entities.historic import Historic as HistoricEntity
from source.entities.prophesy import Prophesy as ProphesyEntity
from source.enumerators.historic import Historic as HistoricEnum
from source.libraries.database.transaction import TransactionLib

# class Result:

#     @property
#     def type(self) -> HistoricEnum:
#         return HistoricEnum(self._type)

#     @type.setter
#     def type(self, value: HistoricEnum):
#         self._type = value.value

#     @property
#     def increased(self) -> int:
#         return self._increased

#     @increased.setter
#     def increased(self, value: int):
#         self._increased = value

#     @property
#     def date(self) -> datetime:
#         return datetime.fromtimestamp(self._date)

#     @date.setter
#     def date(self, value: datetime):
#         self._date = value.timestamp()

#     @property
#     def trend(self) -> float:
#         return self._trend

#     @trend.setter
#     def trend(self, value: float):
#         self._trend = value

#     @property
#     def yhat_lower(self) -> float:
#         return self._yhat_lower

#     @yhat_lower.setter
#     def yhat_lower(self, value: float):
#         self._yhat_lower = value

#     @property
#     def yhat_upper(self) -> float:
#         return self._yhat_upper

#     @yhat_upper.setter
#     def yhat_upper(self, value: float):
#         self._yhat_upper = value

#     @property
#     def trend_lower(self) -> float:
#         return self._trend_lower

#     @trend_lower.setter
#     def trend_lower(self, value: float):
#         self._trend_lower = value

#     @property
#     def trend_upper(self) -> float:
#         return self._trend_upper

#     @trend_upper.setter
#     def trend_upper(self, value: float):
#         self._trend_upper = value

#     @property
#     def additive_terms(self) -> float:
#         return self._additive_terms

#     @additive_terms.setter
#     def additive_terms(self, value: float):
#         self._additive_terms = value

#     @property
#     def additive_terms_lower(self) -> float:
#         return self._additive_terms_lower

#     @additive_terms_lower.setter
#     def additive_terms_lower(self, value: float):
#         self._additive_terms_lower = value

#     @property
#     def additive_terms_upper(self) -> float:
#         return self._additive_terms_upper

#     @additive_terms_upper.setter
#     def additive_terms_upper(self, value: float):
#         self._additive_terms_upper = value

#     @property
#     def weekly(self) -> float:
#         return self._weekly

#     @weekly.setter
#     def weekly(self, value: float):
#         self._weekly = value

#     @property
#     def weekly_lower(self) -> float:
#         return self._weekly_lower

#     @weekly_lower.setter
#     def weekly_lower(self, value: float):
#         self._weekly_lower = value

#     @property
#     def weekly_upper(self) -> float:
#         return self._weekly_upper

#     @weekly_upper.setter
#     def weekly_upper(self, value: float):
#         self._weekly_upper = value

#     @property
#     def multiplicative_terms(self) -> float:
#         return self._multiplicative_terms

#     @multiplicative_terms.setter
#     def multiplicative_terms(self, value: float):
#         self._multiplicative_terms = value

#     @property
#     def multiplicative_terms_lower(self) -> float:
#         return self._multiplicative_terms_lower

#     @multiplicative_terms_lower.setter
#     def multiplicative_terms_lower(self, value: float):
#         self._multiplicative_terms_lower = value

#     @property
#     def multiplicative_terms_upper(self) -> float:
#         return self._multiplicative_terms_upper

#     @multiplicative_terms_upper.setter
#     def multiplicative_terms_upper(self, value: float):
#         self._multiplicative_terms_upper = value

#     @property
#     def yhat(self) -> float:
#         return self._yhat

#     @yhat.setter
#     def yhat(self, value: float):
#         self._yhat = value

# encapsulamento para manipular a biblioteca Prophet para prever valoes futuros de acoes de empresas
class Prophet:

    def __init__(self, results: list[HistoricEnum], period: PeriodEnum):
        # y: dados
        # ds: data
        # cap: limite superior
        # floor: limite inferior
        # holiday: datas de feriados ou eventos
        self._period = period
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
        self._transaction = TransactionLib()
        
    def set_historical(self, historical: list[HistoricEntity]):
        self._historical = historical
        self._open_data = None
        self._close_data = None
        self._open_forecast = None
        self._close_forecast = None
        if self._is_open:
            self._open_data = pandas.DataFrame(columns=[
                'ds',
                'y',
                'cap',
                'floor',
            ])
        if self._is_close:
            self._close_data = pandas.DataFrame(columns=[
                'ds',
                'y',
                'cap',
                'floor',
            ])
        i = 0
        for historic in historical:
            if self._is_open:
                self._open_data.loc[i] = [
                    historic.date,
                    historic.open,
                    historic.high,
                    historic.low,
                ]
            if self._is_close:
                self._close_data.loc[i] = [
                    historic.date,
                    historic.close,
                    historic.high,
                    historic.low,
                ]
            i += 1
        self._last = historical[i - 1]
        self._first = historical[0]

    def handle(self):
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

    def _get_forecast(self, data):
        self._prophet = Library(
            daily_seasonality=True,
            yearly_seasonality=False,
            weekly_seasonality=True,
            changepoint_prior_scale=0.01,
            seasonality_prior_scale=1.0,
            seasonality_mode='multiplicative',
        )
        self._prophet.fit(data)
        self._future = self._prophet.make_future_dataframe(periods=self._period.value)
        return self._prophet.predict(self._future)
    
    def _persist(self, forecast) -> list[ProphesyEntity]:
        if forecast is None:
            return []
        day = 0
        end = self._last
        result = []
        for forecast in forecast.to_dict('records'):
            if end.date.timestamp() > forecast['ds'].timestamp():
                continue
            model = ProphesyEntity()
            for key, value in forecast.items():
                if key == 'ds':
                    key = 'date'
                setattr(model, key, value)
            if model.date > end.date:
                day += 1
                model.increased = day
                result.append(model)
        del day
        del end
        return result
    
    # def _results(self, forecast) -> list[Result]:
    #     if forecast is None:
    #         return []
    #     day = 0
    #     end = self._last
    #     results = []
    #     for forecast in forecast.to_dict('records'):
    #         if end.date.timestamp() > forecast['ds'].timestamp():
    #             continue
    #         result = Result()
    #         for key, value in forecast.items():
    #             if key == 'ds':
    #                 key = 'date'
    #             setattr(result, key, value)
    #         if result.date > end.date:
    #             day += 1
    #             result.increased = day
    #             results.append(result)
    #     del day
    #     del end
    #     return results