import sqlite3
from source.libraries.ProphetLib import ProphetLib
from source.services.StockService import StockService
from source.services.HistoricalService import HistoricalService

conn = sqlite3.connect('./storage/wallet.db')
cursor = conn.cursor()

stockService = StockService(cursor)
historicalService = HistoricalService(cursor)

stocks = stockService.getAll()

for stock in stocks:
    print('processando ' + stock.symbol + ' de ' + stock.name)
    historical = historicalService.getAllFromStock(stock)
    end = historical.pop()
    prophet = ProphetLib(historical)
    prophet.handle(60)
    items = prophet.result()
    for item in items:
        print(item.date.strftime('%Y-%m-%d') + ': ' + str(item.yhat))