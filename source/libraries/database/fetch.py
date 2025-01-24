from .query import Query
from django.db import connection

class Fetch:

    def all(self, query: Query) -> list[dict]:
        sql = query.assemble()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                names = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                results = []
                for row in rows:
                    results.append(dict(zip(names, row)))
                return results
            return []
        except Exception as error:
            message = f'Error executing query: {sql} - {error}'
            raise Exception(message)

    def row(self, query: Query) -> dict:
        results = self.all(query)
        for result in results:
            return result
        return None

    def one(self, query: Query):
        sql = query.assemble()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                for row in rows:
                    return row[0]
            return None
        except Exception as error:
            message = f'Error executing query: {sql} - {error}'
            raise Exception(message)
    
    def execute(self, query: Query):
        sql = query.assemble()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
        except Exception as error:
            message = f'Error executing query: {sql} - {error}'
            raise Exception(message)