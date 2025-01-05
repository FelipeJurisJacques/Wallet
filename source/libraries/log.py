from datetime import datetime

class LogLib:

    def __init__(self, log, error):
        self._log = log
        self._error = error

    def log(self, message: str):
        self._log.write(message)

    def date(self, time: datetime) -> str:
        return str(time.day) + '/' + str(time.month) + '/' + str(time.year)