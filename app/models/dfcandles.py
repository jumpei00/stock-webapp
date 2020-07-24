from app.models.candle import StockData
from app.technical import trend
from app.technical import oscillator


class DataFrameCandle(object):
    def __init__(self):
        self.candles = StockData.get_all_candles()
        self.sma = []
        self.ema = []
        self.bbands = trend.BBands(closes=[], n=0, k=0)
        self.ichimoku_cloud = trend.IchimokuCloud(closes=[])
        self.rsi = oscillator.RSI(closes=[], period=0)
        self.macd = oscillator.MACD(
            closes=[], fast_period=0, slow_period=0, signal_period=0)
        self.willr = oscillator.WILLR(highs=[], lows=[], closes=[], period=0)
        self.stochf = oscillator.STOCHF(
            highs=[], lows=[], closes=[], fastk_period=0, fastd_period=0)
        self.stoch = oscillator.STOCH(
            highs=[], lows=[], closes=[], fastk_period=0, slowk_period=0, slowd_period=0
        )

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
            sma = trend.SMA(
                closes=self.closes,
                period=period
            )
            self.sma.append(sma)
            return True
        return False

    def add_ema(self, period):
        if len(self.closes) > period:
            ema = trend.EMA(
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

    def add_rsi(self, period):
        if len(self.closes) > period:
            self.rsi = oscillator.RSI(
                closes=self.closes,
                period=period
            )
            return True
        return False

    def add_macd(self, fast_period, slow_period, signal_period):
        if len(self.closes) > 1:
            self.macd = oscillator.MACD(
                closes=self.closes,
                fast_period=fast_period,
                slow_period=slow_period,
                signal_period=signal_period
            )
            return True
        return False

    def add_willr(self, period):
        if len(self.closes) > 1:
            self.willr = oscillator.WILLR(
                highs=self.highs,
                lows=self.lows,
                closes=self.closes,
                period=period
            )
            return True
        return False

    def add_stochf(self, fastk_period, fastd_period):
        if len(self.closes) > 1:
            self.stochf = oscillator.STOCHF(
                highs=self.highs,
                lows=self.lows,
                closes=self.closes,
                fastk_period=fastk_period,
                fastd_period=fastd_period
            )
            return True
        return False

    def add_stoch(self, fastk_period, slowk_period, slowd_period):
        if len(self.closes) > 1:
            self.stoch = oscillator.STOCH(
                highs=self.highs,
                lows=self.lows,
                closes=self.closes,
                fastk_period=fastk_period,
                slowk_period=slowk_period,
                slowd_period=slowd_period
            )
            return True
        return False
