import pandas as pd
import sqlite3
import datetime
import yfinance
from pandas_datareader import data
from source.services.StockService import StockService
from source.services.HistoricalService import HistoricalService

conn = sqlite3.connect('./storage/wallet.db')
cursor = conn.cursor()

stockService = StockService(cursor)
historicalService = HistoricalService(cursor)

symbols = stockService.getSymbols()
for symbol in symbols:
    end = datetime.datetime.now().strftime('%Y-%m-%d')
    start = historicalService.getMaxDate(symbol).strftime('%Y-%m-%d')
    print(yfinance.download(symbol, start=start, end=end))
    #print(data.get_data_yahoo(symbol, start=start, end=end))

conn.close()
