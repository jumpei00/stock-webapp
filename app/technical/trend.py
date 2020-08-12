import numpy as np

import talib

from app.technical.serializer import Serializer
from utils.utils import ichimoku_cloud
from utils.utils import nan_to_zero


class SMA(Serializer):
    def __init__(self, closes, period):
        self.period = period
        self.values = self.sma(closes=closes)

    def sma(self, closes):
        values = talib.SMA(np.asarray(closes), self.period)
        return nan_to_zero(values).tolist()


class EMA(Serializer):
    def __init__(self, closes, period):
        self.period = period
        self.values = self.ema(closes=closes)

    def ema(self, closes):
        values = talib.EMA(np.asarray(closes), self.period)
        return nan_to_zero(values).tolist()


class BBands(Serializer):
    def __init__(self, closes, n, k):
        self.n = n
        self.k = k
        self.up, self.mid, self.down = self.bbands(closes=closes)

    def bbands(self, closes):
        if not closes:
            return [], [], []
        up, mid, down = talib.BBANDS(
            np.asarray(closes), self.n, self.k, self.k, 0
        )
        up_list = nan_to_zero(up).tolist()
        mid_list = nan_to_zero(mid).tolist()
        down_list = nan_to_zero(down).tolist()
        return up_list, mid_list, down_list


class IchimokuCloud(Serializer):
    def __init__(self, closes):
        self.tenkan, self.kijun, self.senkou_a, \
            self.senkou_b, self.chikou = ichimoku_cloud(in_real=closes)
