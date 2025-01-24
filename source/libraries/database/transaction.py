from django.db import transaction

class Transaction:

    def begin(self):
        transaction.set_autocommit(False)

    def commit(self):
        transaction.commit()
        transaction.set_autocommit(True)

    def rollback(self):
        transaction.rollback()
        transaction.set_autocommit(True)