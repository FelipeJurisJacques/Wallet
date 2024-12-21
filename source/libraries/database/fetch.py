from .query import QueryLib
from django.db import connection

class FetchLib:

    def all(self, query:QueryLib) -> list[dict]:
        with connection.cursor() as cursor:
            cursor.execute(query.assemble())
            names = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append(dict(zip(names, row)))
            return results
        return []

    def row(self, query:QueryLib) -> dict:
        results = self.all(query.assemble())
        for result in results:
            return result
        return None

    def one(self, query:QueryLib):
        with connection.cursor() as cursor:
            cursor.execute(query.assemble())
            rows = cursor.fetchall()
            for row in rows:
                return row[0]
        return None