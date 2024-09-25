import sqlite3
from source.libraries.DriveLib import DriveLib
from source.libraries.ProphetLib import ProphetLib
from source.libraries.StrategyLib import StrategyLib
from source.services.StockService import StockService
from source.services.HistoricalService import HistoricalService

conn = sqlite3.connect('./storage/wallet.db')
cursor = conn.cursor()

stockService = StockService(cursor)
historicalService = HistoricalService(cursor)

stocks = stockService.getAll()

for stock in stocks:
    print('processando ' + stock.symbol + ' de ' + stock.name)
    i = 0
    end = None
    drive = DriveLib()
    drive.getUserWallet().value = 1000.0
    print('Valor inicial R$ ' + str(drive.getUserWallet().value))
    strategy = StrategyLib()
    while i < 5:
        historical = historicalService.getPeriodFromStock(stock, 366, i)
        i += 1
        end = historical.pop()
        prophet = ProphetLib(historical)
        prophet.handle(60)
        forecast = prophet.result()
        strategy.handle(drive.getUserWallet(), drive.getUserStock(), historical, forecast)
        decision = strategy.result
        if decision > 0:
            drive.buy(end.close, decision)
        if decision < 0:
            drive.sell(end.close, decision * -1)
    drive.sell(end.close, drive.sellable())
    print('Valor total R$ ' + str(drive.getUserWallet().value))