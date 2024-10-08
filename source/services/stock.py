import sqlite3
from ..models.stock import StockModel
from ..entities.stock import StockEntity

class StockService:
    def __init__(self, cursor:sqlite3.Cursor):
        self.cursor = cursor
    
    def all(self) -> list[StockModel]:
        result = []
        for entity in StockEntity.all():
            result.append(StockModel(entity))
        return result