class HistoricEntity:
    def __init__(self, id, stock_id, date, open, high, low, close, volume):
        self.id = id
        self.low = low
        self.date = date
        self.high = high
        self.open = open
        self.close = close
        self.volume = volume
        self.stock_id = stock_id