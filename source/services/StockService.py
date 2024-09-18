import sqlite3
from ..model.StockModel import StockModel
from ..entities.StockEntity import StockEntity

class StockService:
    def __init__(self, cursor:sqlite3.Cursor):
        self.cursor = cursor

    def getSymbols(self) -> list[str]:
        self.cursor.execute("SELECT symbol FROM stocks")
        names = []
        stocks = self.cursor.fetchall()
        for stock in stocks:
            names.append(stock[0])
        return names
    
    def getAll(self) -> list[StockModel]:
        self.cursor.execute("SELECT * FROM stocks")
        names = []
        stocks = self.cursor.fetchall()
        for stock in stocks:
            names.append(StockModel(StockEntity(
                stock[0],
                stock[1],
                stock[2],
                stock[3],
                stock[4]
            )))
        return names