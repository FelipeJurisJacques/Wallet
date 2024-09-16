import sqlite3
import datetime

class HistoricalService:
    def __init__(self, cursor:sqlite3.Cursor):
        self.cursor = cursor

    def getMaxDate(self, symbol):
        return datetime.datetime.now() - datetime.timedelta(days=2*365)
        query = f"SELECT MAX(h.date) FROM historical AS h INNER JOIN stocks AS s ON s.id = h.stock_id WHERE s.stock = ?"
        self.cursor.execute(query, symbol)
        last_date = self.cursor.fetchone()[0]
        if last_date:
            return pd.to_datetime(last_date) + pd.Timedelta(days=1)
        else:
            return None