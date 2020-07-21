from app.models.candle import StockData
from app.technical import trend


class DataFrameCandle(object):
    def __init__(self):
        self.candles = StockData.get_all_candles()
        self.sma = []
        self.ema = []
        self.bbands = trend.BBands([], 0, 0)
        self.ichimoku_cloud = trend.IchimokuCloud([], [], [], [], [])

    # Return this dictionary to webserver
    @property
    def values(self):
        return {
            'candles': [c.values for c in self.candles]
        }

    @property
    def opens(self):
        values = []
        for candle in self.candles:
            values.append(candle.open)
        return values

    @property
    def closes(self):
        values = []
        for candle in self.candles:
            values.append(candle.close)
        return values

    @property
    def highs(self):
        values = []
        for candle in self.candles:
            values.append(candle.high)
        return values

    @property
    def lows(self):
        values = []
        for candle in self.candles:
            values.append(candle.low)
        return values

    @property
    def volumes(self):
        values = []
        for candle in self.candles:
            values.append(candle.volume)
        return values

    def add_sma(self, period):
        if len(self.closes) > period:
            sma = trend.Sma(
                closes=self.closes,
                period=period
            )
            self.sma.append(sma)
            return True
        return False

    def add_ema(self, period):
        if len(self.closes) > period:
            ema = trend.Ema(
                closes=self.closes,
                period=period
            )
            self.ema.append(ema)
            return True
        return False

    def add_bbands(self, n, k):
        if n <= len(self.closes):
            self.bbands = trend.BBands(
                closes=self.closes,
                n=n,
                k=k
            )
            return True
        return False

    def add_ichimoku(self):
        if len(self.closes) >= 9:
            self.ichimoku_cloud = trend.IchimokuCloud(
                closes=self.closes
            )
            return True
        return False
