from .query import Query
from django.db import connection

class Fetch:

    def all(self, query: Query) -> list[dict]:
        with connection.cursor() as cursor:
            cursor.execute(query.assemble())
            names = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append(dict(zip(names, row)))
            return results
        return []

    def row(self, query: Query) -> dict:
        results = self.all(query)
        for result in results:
            return result
        return None

    def one(self, query: Query):
        with connection.cursor() as cursor:
            cursor.execute(query.assemble())
            rows = cursor.fetchall()
            for row in rows:
                return row[0]
        return None
    
    def execute(self, query: Query):
        with connection.cursor() as cursor:
            cursor.execute(query.assemble())