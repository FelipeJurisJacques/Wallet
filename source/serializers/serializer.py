class Serializer:

    def __init__(self):
        self._data = self.handle()

    def handle(self) -> str:
        return {}

    @property
    def data(self):
        return self._data