class Serializer:

    def __init__(self):
        self._data = {}
        self.handle()

    def handle(self):
        pass

    @property
    def data(self):
        return self._data