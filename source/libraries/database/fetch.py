from django.db import connection

class FetchLib:

    def all(self, query):
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
        return []

    def row(self, query):
        results = self.all(query)
        for result in results:
            return result
        return None

    def one(self, query):
        result = self.row(query)
        if result is None:
            return None
        else:
            return result[0]