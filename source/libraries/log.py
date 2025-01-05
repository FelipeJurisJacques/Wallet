from datetime import datetime

class LogLib:

    def __init__(self, log, error):
        self._log = log
        self._error = error

    def log(self, message: str):
        self._log.write(message)

    def date(self, time: datetime) -> str:
        if time is None:
            return ''
        return time.strftime("%d/%m/%Y")
        # return time.strftime("%d/%m/%Y %H:%M:%S")

    def money(self, value) -> str:
        if value is None:
            return ''
        return "{:.2f}".format(value)