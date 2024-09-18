import pandas
import sqlite3
from prophet import Prophet
from source.services.StockService import StockService
from source.services.HistoricalService import HistoricalService

conn = sqlite3.connect('./storage/wallet.db')
cursor = conn.cursor()

stockService = StockService(cursor)
historicalService = HistoricalService(cursor)

stocks = stockService.getAll()

for stock in stocks:
    historical = historicalService.getAllFromStock(stock)
    # y: dados
    # ds: data
    # cap: limite superior
    # floor: limite inferior
    # holiday: datas de feriados ou eventos
    data = pandas.DataFrame(columns=['ds', 'y'])
    for historic in historical:
        data.loc[len(data)] = [historic.date, historic.close]
    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    model.plot(forecast)
    print(forecast.tail(30))