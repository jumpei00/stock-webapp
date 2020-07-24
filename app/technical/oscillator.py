import numpy as np

import talib

from app.technical.serializer import Serializer
from utils.utils import nan_to_zero


class RSI(Serializer):
    def __init__(self, closes, period):
        self.period = period
        self.values = self.rsi(closes=closes)

    def rsi(self, closes):
        if not closes:
            return []
        values = talib.RSI(np.asarray(closes), self.period)
        return nan_to_zero(values).tolist()


class MACD(Serializer):
    def __init__(self, closes, fast_period, slow_period, signal_period):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        self.macd, self.macd_signal, self.macd_hist = self.macd(closes=closes)

    def macd(self, closes):
        if not closes:
            return [], [], []
        macd, macd_signal, macd_hist = talib.MACD(
            np.asarray(closes),
            self.fast_period, self.slow_period, self.signal_period
        )
        macd_list = nan_to_zero(macd).tolist()
        macd_signal_list = nan_to_zero(macd_signal).tolist()
        macd_hist_list = nan_to_zero(macd_hist).tolist()
        return macd_list, macd_signal_list, macd_hist_list


class WILLR(Serializer):
    def __init__(self, highs, lows, closes, period):
        self.period = period
        self.values = self.willr(highs=highs, lows=lows, closes=closes)

    def willr(self, highs, lows, closes):
        if not highs or not lows or not closes:
            return []
        values = talib.WILLR(
            np.asarray(highs), np.asarray(lows), np.asarray(closes),
            self.period
        )
        return nan_to_zero(values).tolist()


class STOCHF(Serializer):
    def __init__(self, highs, lows, closes, fastk_period, fastd_period):
        self.fastk_period = fastk_period
        self.fastd_period = fastd_period
        self.fastk, self.fastd = self.stochf(
            highs=highs, lows=lows, closes=closes)

    def stochf(self, highs, lows, closes):
        if not highs or not lows or not closes:
            return [], []
        fastk, fastd = talib.STOCHF(
            np.asarray(highs), np.asarray(lows), np.asarray(closes),
            self.fastk_period, self.fastd_period, 0
        )
        fastk_list = nan_to_zero(fastk).tolist()
        fastd_list = nan_to_zero(fastd).tolist()
        return fastk_list, fastd_list


class STOCH(Serializer):
    def __init__(self, highs, lows, closes,
                 fastk_period, slowk_period, slowd_period):
        self.fastk_period = fastk_period
        self.slowk_period = slowk_period
        self.slowd_period = slowd_period

    def stoch(self, highs, lows, closes):
        if not highs or not lows or not closes:
            return [], []
        slowk, slowd = talib.STOCH(
            np.asarray(highs), np.asarray(lows), np.asarray(closes),
            self.fastk_period, self.slowk_period, 0, self.slowd_period, 0
        )
        slowk_list = nan_to_zero(slowk).tolist()
        slowd_list = nan_to_zero(slowd).tolist()
        return slowk_list, slowd_list
