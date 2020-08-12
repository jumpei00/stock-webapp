import omitempty

from app.models.candle import StockData
from app.models.events import BackTestParamsController
from app.models.events import SignalEventController
from app.technical import trend
from app.technical import oscillator
from utils.utils import empty_to_none
import settings
import constants


class DataFrameCandle(object):
    def __init__(self, code, duration=settings.duration_defalut):
        self.code = code
        self.candles = StockData.get_some_candles(limit=duration)
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
            highs=[], lows=[], closes=[], fastk_period=0, slowk_period=0, slowd_period=0)
        self.back_test_params = BackTestParamsController(code=self.code)
        self.today_trade = {}
        self.each_event = {}

    @property
    def chart_values(self):
        return {
            'candles': [c.values for c in self.candles],
            'smas': empty_to_none([s.value for s in self.sma]),
            'emas': empty_to_none([s.value for s in self.ema]),
            'bbands': self.bbands.value,
            'ichimoku': self.ichimoku_cloud.value,
            'rsi': self.rsi.value,
            'macd': self.macd.value,
            'willr': self.willr.value,
            'stochf': self.stochf.value,
            'stoch': self.stoch.value,
            'events': empty_to_none(self.each_event)
        }

    @property
    def trade_values(self):
        return {
            'params': self.back_test_params.value,
            'trade': empty_to_none(self.today_trade)
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

    def add_params(self):
        back_test_params = self.back_test_params.get_params
        if not back_test_params.params:
            return False
        self.back_test_params = back_test_params
        return True

    def add_each_event(self, ema_enable, bb_enable, ichimoku_enable, rsi_enble,
                       macd_enable, willr_enable, stochf_enable, stoch_enable):
        signal_events = constants.SIGNAL_EVENTS
        enables = [ema_enable, bb_enable, ichimoku_enable, rsi_enble,
                   macd_enable, willr_enable, stochf_enable, stoch_enable]
        base_list = constants.BASE_LIST

        for signal_events_key, enable, base in zip(signal_events, enables, base_list):
            if enable:
                signal_event = SignalEventController.get_signal_events_for_code(
                    base=base, code=self.code)
                signal_events[signal_events_key] = signal_event.value

        self.each_event = omitempty(signal_events)

        return True
