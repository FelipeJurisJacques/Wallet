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
    drive = DriveLib()
    wallet = drive.getUserWallet()
    wallet.value = 1000.0
    strategy = StrategyLib()
    while i < 1:
        historical = historicalService.getPeriodFromStock(stock, 366, i)
        i += 1
        prophet = ProphetLib(historical)
        prophet.handle(60)
        forecast = prophet.result()
        strategy.handle(wallet, drive.getUserStock(), historical, forecast)
        decision = strategy.result
        if decision == 0:
            print('Não fazer nada')
        if decision > 0:
            print('Comprar as ações')
        if decision < 0:
            print('Vender as ações')