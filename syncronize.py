import sqlite3
import datetime
import yfinance
from source.services.StockService import StockService
from source.services.HistoricalService import HistoricalService

conn = sqlite3.connect('./storage/wallet.db')
cursor = conn.cursor()

stockService = StockService(cursor)
historicalService = HistoricalService(cursor)

stocks = stockService.getAll()
for stock in stocks:
    end = datetime.datetime.now().strftime('%Y-%m-%d')
    start = historicalService.getMaxDate(stock).strftime('%Y-%m-%d')
    response = yfinance.download(stock.symbol, start=start, end=end)
    if not response.empty:
        for item in response.itertuples():
            historicalService.add(
                stock,
                item.Index,
                item.Open,
                item.High,
                item.Low,
                item.Close,
                item.Volume
            )
            print(item)

conn.close()
