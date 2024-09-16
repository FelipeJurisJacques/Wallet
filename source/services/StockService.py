import sqlite3
from ..model.StockModel import StockModel

class StockService:
    def __init__(self, cursor:sqlite3.Cursor):
        self.cursor = cursor

    def getSymbols(self):
        self.cursor.execute("SELECT symbol FROM stocks")
        names = []
        stocks = self.cursor.fetchall()
        for stock in stocks:
            names.append(stock[0])
        return names
    
    def getAll(self):
        self.cursor.execute("SELECT * FROM stocks")
        names = []
        stocks = self.cursor.fetchall()
        for stock in stocks:
            names.append(StockModel(stock[0], stock[1], stock[2], stock[3], stock[4]))
        return names