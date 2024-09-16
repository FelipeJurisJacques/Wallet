import sqlite3

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