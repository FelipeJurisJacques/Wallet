import sqlite3
import datetime
from ..model.StockModel import StockModel

class HistoricalService:
    def __init__(self, cursor:sqlite3.Cursor):
        self.cursor = cursor

    def getMaxDate(self, stock:StockModel):
        return datetime.datetime.now() - datetime.timedelta(days=20)
        query = f"SELECT MAX(date) FROM historical WHERE stock_id = ?"
        self.cursor.execute(query, stock.id)
        last_date = self.cursor.fetchone()[0]
        if last_date:
            return pd.to_datetime(last_date) + pd.Timedelta(days=1)
        else:
            return None
        
    def add(self, stock:StockModel, date, open, high, low, close, volume):
        self.cursor.execute(
            "INSERT INTO historical (stock_id, date, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (stock.id, date.timestamp(), open, high, low, close, volume)
        )