import numpy as np

import talib

from app.technical.serializer import Serializer
from utils.utils import nan_to_zero


class Sma(Serializer):
    def __init__(self, closes, period):
        self.period = period
        self.values = self.sma(closes=closes)

    def sma(self, closes):
        values = talib.SMA(np.asarray(closes), self.period)
        return nan_to_zero(values).tolist()


class Ema(Serializer):
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
        up, mid, down = talib.BBANDS(
            np.asarray(self.closes), self.n, self.k, self.k, 0
        )
        up_list = nan_to_zero(up).tolist()
        mid_list = nan_to_zero(mid).tolist()
        down_list = nan_to_zero(down).tolist()
        return up_list, mid_list, down_list


class IchimokuCloud(Serializer):
    def __init__(self, closes):
        self.tenkan, self.kijun, self.senkou_a, \
            self.senkou_b, self.chikou = self.ichimoku_cloud(in_real=closes)

    def ichimoku_cloud(self, in_real):
        length = len(in_real)
        tenkan = [0] * min(9, length)
        kijun = [0] * min(26, length)
        senkou_a = [0] * min(26, length)
        senkou_b = [0] * min(52, length)
        chikou = [0] * min(26, length)
        for i in range(length):
            if i >= 9:
                min_val, max_val = self.min_max(in_real[i - 9:i])
                tenkan.append((min_val + max_val) / 2)
            if i >= 26:
                min_val, max_val = self.min_max(in_real[i - 26:i])
                kijun.append((min_val + max_val) / 2)
                senkou_a.append((tenkan[i] + kijun[i]) / 2)
                chikou.append(in_real[i - 26])
            if i >= 52:
                min_val, max_val = self.min_max(in_real[i - 52:i])
                senkou_b.append((min_val + max_val) / 2)

        senkou_a = ([0] * 26) + senkou_a[:-26]
        senkou_b = ([0] * 26) + senkou_b[:-26]
        return tenkan, kijun, senkou_a, senkou_b, chikou

    def min_max(self, in_real):
        min_val = in_real[0]
        max_val = in_real[0]
        for price in in_real:
            if min_val > price:
                min_val = price
            if max_val < price:
                max_val = price
        return min_val, max_val
