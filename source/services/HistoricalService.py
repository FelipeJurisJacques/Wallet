import sqlite3
import datetime
from ..model.StockModel import StockModel
from ..model.HistoricModel import HistoricModel
from ..entities.HistoricEntity import HistoricEntity

class HistoricalService:
    def __init__(self, cursor:sqlite3.Cursor):
        self.cursor = cursor

    def getAllFromStock(self, stock:StockModel) -> list[HistoricModel]:
        self.cursor.execute(
            "SELECT id, stock_id, date, open, high, low, close, volume FROM historical WHERE stock_id = ?",
            (stock.getId(),)
        )
        list = []
        rows = self.cursor.fetchall()
        for row in rows:
            list.append(HistoricModel(HistoricEntity(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7]
            )))
        return list

    def getMaxDate(self, stock:StockModel) -> datetime.date:
        self.cursor.execute(
            "SELECT MAX(date) FROM historical WHERE stock_id = ?",
            (stock.getId(),)
        )
        row = self.cursor.fetchone()
        if row[0]:
            return datetime.date.fromtimestamp(row[0])
        else:
            return datetime.date.now() - datetime.timedelta(days=2*365)

    def add(self, stock:StockModel, date, open, high, low, close, volume):
        self.cursor.execute(
            "INSERT INTO historical (stock_id, date, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (stock.getId(), date.timestamp(), open, high, low, close, volume)
        )