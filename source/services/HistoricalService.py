import sqlite3
import datetime
from ..model.StockModel import StockModel

class HistoricalService:
    def __init__(self, cursor:sqlite3.Cursor):
        self.cursor = cursor

    def getMaxDate(self, stock:StockModel):
        self.cursor.execute(
            "SELECT MAX(date) FROM historical WHERE stock_id = ?",
            (stock.id,)
        )
        row = self.cursor.fetchone()
        if row[0]:
            return datetime.datetime.fromtimestamp(row[0])
        else:
            return datetime.datetime.now() - datetime.timedelta(days=2*365)
        
    def add(self, stock:StockModel, date, open, high, low, close, volume):
        self.cursor.execute(
            "INSERT INTO historical (stock_id, date, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (stock.id, date.timestamp(), open, high, low, close, volume)
        )