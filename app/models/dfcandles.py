from app.models.candle import StockData


class DataFrameCandle(object):
    def __init__(self):
        self.candle_cls = []

    @property
    def values(self):
        return {
            'candles': [c.values for c in self.candle_cls]
        }

    def set_all_candle_cls(self):
        self.candle_cls = StockData.get_all_candles()
        return True
