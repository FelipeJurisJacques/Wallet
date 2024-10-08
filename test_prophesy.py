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
    future = None
    drive = DriveLib()
    drive.getUserWallet().value = 1000.0
    print('Valor inicial R$ ' + str(drive.getUserWallet().value))
    strategy = StrategyLib()
    while i < 20:
        historical = historicalService.getPeriodFromStock(stock, 40, i)
        i += 1
        future = historical.pop()
        prophet = ProphetLib(historical)
        prophet.handle(60)
        forecast = prophet.result()
        if len(forecast) == 0:
            print('Sem previsao')
        else:
            strategy.handle(
                drive.getUserWallet(),
                drive.getUserStock(),
                historical[-1],
                forecast[0],
                future
            )
            decision = strategy.result
            if decision > 0:
                drive.buy(historical[-1].close, decision)
            if decision < 0:
                drive.sell(historical[-1].close, decision * -1)
    drive.sell(future.close, drive.sellable())
    print('Valor total R$ ' + str(drive.getUserWallet().value))