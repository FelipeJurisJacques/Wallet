import pandas
import sqlite3
from prophet import Prophet
from source.services.StockService import StockService
from source.services.ProphetService import ProphetService
from source.services.HistoricalService import HistoricalService

conn = sqlite3.connect('./storage/wallet.db')
cursor = conn.cursor()

stockService = StockService(cursor)
historicalService = HistoricalService(cursor)

stocks = stockService.getAll()

for stock in stocks:
    print('processando ' + stock.symbol + ' de ' + stock.name)
    historical = historicalService.getAllFromStock(stock)
    prophet = ProphetService(historical)
    prophet.handle(60)
    items = prophet.result()
    for item in items:
        print(item.date.strftime('%Y-%m-%d') + ': ' + str(item.yhat))