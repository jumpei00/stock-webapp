import logging
import numpy as np

import talib

from app.models.events import SignalEventController
from utils.utils import ichimoku_cloud
import constants

logger = logging.getLogger(__name__)


class BackTestingSerializer(object):
    def __init__(self, code, candles, highs, lows, closes):
        self.ema = Ema(code=code, candles=candles, closes=closes)
        self.bbands = BBands(code=code, candles=candles, closes=closes)
        self.ichimoku = Ichimoku(code=code, candles=candles, closes=closes)
        self.rsi = Rsi(code=code, candles=candles, closes=closes)
        self.macd = Macd(code=code, candles=candles, closes=closes)
        self.willr = Willr(code=code, candles=candles, highs=highs,
                           lows=lows, closes=closes)
        self.stochf = Stochf(code=code, candles=candles, highs=highs,
                             lows=lows, closes=closes)
        self.stoch = Stoch(code=code, candles=candles, highs=highs,
                           lows=lows, closes=closes)


class Ema(object):
    def __init__(self, code, candles, closes):
        self.code = code
        self.candles = candles
        self.closes = closes

    def back_test(self, short_period, long_period, base=constants.BACKTEST,
                  backtest=False, save=False):
        if len(self.candles) <= short_period or len(self.candles) <= long_period:
            return None

        signal_event_controller = SignalEventController(base=base)
        if base == constants.EMA and save:
            signal_event_controller.delete(code=self.code)

        ema_value_short = talib.EMA(np.asarray(self.closes), short_period)
        ema_value_long = talib.EMA(np.asarray(self.closes), long_period)

        for day in range(1, len(self.candles)):
            if day < short_period or day < long_period:
                continue
            if day == len(self.candles) - 1 and backtest:
                continue

            if ema_value_short[day - 1] < ema_value_long[day - 1] and ema_value_short[day] > ema_value_long[day]:
                if day == len(self.candles) - 1:
                    signal_date = self.candles[day].date
                    traded_date = None
                    price = None
                else:
                    signal_date = self.candles[day].date
                    traded_date = self.candles[day + 1].date
                    price = self.candles[day + 1].open

                signal_event_controller.buy(
                    code=self.code,
                    signal_date=signal_date,
                    traded_date=traded_date,
                    price=price,
                    save=save
                )
            elif ema_value_short[day - 1] > ema_value_long[day - 1] and ema_value_short[day] < ema_value_long[day]:
                if day == len(self.candles) - 1:
                    signal_date = self.candles[day].date
                    traded_date = None
                    price = None
                else:
                    signal_date = self.candles[day].date
                    traded_date = self.candles[day + 1].date
                    price = self.candles[day + 1].open

                signal_event_controller.sell(
                    code=self.code,
                    signal_date=signal_date,
                    traded_date=traded_date,
                    price=price,
                    save=save
                )

        return signal_event_controller

    def optimization(self, short_period_low, short_period_up, long_period_low, long_period_up):
        logger.info(
            '<action=Ema->>optimization>: Ema backtest and params optimization Start')

        performance = 0
        best_short_period = 0
        best_long_period = 0

        for short_period in range(short_period_low, short_period_up):
            for long_period in range(long_period_low, long_period_up):
                signal_envent_controller = self.back_test(
                    short_period=short_period, long_period=long_period, backtest=True
                )
                if signal_envent_controller is None:
                    continue
                profit = signal_envent_controller.profit
                if performance < profit:
                    performance = profit
                    best_short_period = short_period
                    best_long_period = long_period

        logger.info(
            '<action=Ema->>optimization>: Ema backtest and params optimization End')

        return performance, best_short_period, best_long_period


class BBands(object):
    def __init__(self, code, candles, closes):
        self.code = code
        self.candles = candles
        self.closes = closes

    def back_test(self, n, k, base=constants.BACKTEST, backtest=False, save=False):
        if len(self.candles) <= n:
            return None

        signal_event_controller = SignalEventController(base=base)
        if base == constants.BBANDS and save:
            signal_event_controller.delete(code=self.code)

        bb_up, _, bb_down = talib.BBANDS(np.asarray(self.closes), n, k, k, 0)

        for day in range(1, len(self.candles)):
            if day < n:
                continue
            if day == len(self.candles) - 1 and backtest:
                continue

            if bb_down[day - 1] > self.candles[day - 1].close and bb_down[day] <= self.candles[day].close:
                if day == len(self.candles) - 1:
                    signal_date = self.candles[day].date
                    traded_date = None
                    price = None
                else:
                    signal_date = self.candles[day].date
                    traded_date = self.candles[day + 1].date
                    price = self.candles[day + 1].open

                signal_event_controller.buy(
                    code=self.code,
                    signal_date=signal_date,
                    traded_date=traded_date,
                    price=price,
                    save=save
                )

            elif bb_down[day - 1] < self.candles[day - 1].close and bb_down[day] >= self.candles[day].close:
                if day == len(self.candles) - 1:
                    signal_date = self.candles[day].date
                    traded_date = None
                    price = None
                else:
                    signal_date = self.candles[day].date
                    traded_date = self.candles[day + 1].date
                    price = self.candles[day + 1].open

                signal_event_controller.sell(
                    code=self.code,
                    signal_date=signal_date,
                    traded_date=traded_date,
                    price=price,
                    save=save
                )

        return signal_event_controller

    def optimization(self, n_low, n_up, k_low, k_up):
        logger.info(
            '<action=BBands->>optimization>: BBands backtest and params optimization Start')

        performance = 0
        best_n = 0
        best_k = 0

        for n in range(n_low, n_up):
            for k in np.arange(k_low, k_up, 0.1):
                signal_envent_controller = self.back_test(
                    n=n, k=k, backtest=True)
                if signal_envent_controller is None:
                    continue
                profit = signal_envent_controller.profit
                if performance < profit:
                    performance = profit
                    best_n = n
                    best_k = k

        logger.info(
            '<action=BBands->>optimization>: BBands backtest and params optimization End')

        return performance, best_n, best_k


class Ichimoku(object):
    def __init__(self, code, candles, closes):
        self.code = code
        self.candles = candles
        self.closes = closes

    def back_test(self, base=constants.BACKTEST, backtest=False, save=False):
        if len(self.candles) <= 52:
            return None

        signal_event_controller = SignalEventController(base=base)
        if base == constants.ICHIMOKU and save:
            signal_event_controller.delete(code=self.code)

        tenkan, kijun, senkou_a, senkou_b, chikou = ichimoku_cloud(self.closes)

        for day in range(1, len(self.candles)):
            if day == len(self.candles) - 1 and backtest:
                continue

            if chikou[day - 1] < self.candles[day - 1].high and \
                    chikou[day] >= self.candles[day].high and senkou_a[day] < self.candles[day].low and \
                    senkou_b[day] < self.candles[day].low and tenkan[day] > kijun[day]:
                if day == len(self.candles) - 1:
                    signal_date = self.candles[day].date
                    traded_date = None
                    price = None
                else:
                    signal_date = self.candles[day].date
                    traded_date = self.candles[day + 1].date
                    price = self.candles[day + 1].open

                signal_event_controller.buy(
                    code=self.code,
                    signal_date=signal_date,
                    traded_date=traded_date,
                    price=price,
                    save=save
                )

            elif chikou[day - 1] > self.candles[day - 1].low and \
                    chikou[day] <= self.candles[day].low and senkou_a[day] > self.candles[day].high and \
                    senkou_b[day] > self.candles[day].high and tenkan[day] < kijun[day]:
                if day == len(self.candles) - 1:
                    signal_date = self.candles[day].date
                    traded_date = None
                    price = None
                else:
                    signal_date = self.candles[day].date
                    traded_date = self.candles[day + 1].date
                    price = self.candles[day + 1].open

                signal_event_controller.sell(
                    code=self.code,
                    signal_date=signal_date,
                    traded_date=traded_date,
                    price=price,
                    save=save
                )

        return signal_event_controller

    def optimization(self):
        logger.info(
            '<action=Ichimoku->>optimization>: Ichimoku backtest and params optimization Start')

        signal_envent_controller = self.back_test(backtest=True)
        if signal_envent_controller is None:
            return 0.0

        logger.info(
            '<action=Ichimoku->>optimization>: Ichimoku backtest and params optimization End')

        return signal_envent_controller.profit


class Rsi(object):
    def __init__(self, code, candles, closes):
        self.code = code
        self.candles = candles
        self.closes = closes

    def back_test(self, period, buy_thread, sell_thread, base=constants.BACKTEST,
                  backtest=False, save=False):
        if len(self.candles) <= period:
            return None

        signal_event_controller = SignalEventController(base=base)
        if base == constants.RSI and save:
            signal_event_controller.delete(code=self.code)

        values = talib.RSI(np.asarray(self.closes), period)

        for day in range(1, len(self.candles)):
            if values[day - 1] == 0 or values[day - 1] == 100:
                continue
            if day == len(self.candles) - 1 and backtest:
                continue

            if values[day - 1] < buy_thread and values[day] >= buy_thread:
                if day == len(self.candles) - 1:
                    signal_date = self.candles[day].date
                    traded_date = None
                    price = None
                else:
                    signal_date = self.candles[day].date
                    traded_date = self.candles[day + 1].date
                    price = self.candles[day + 1].open

                signal_event_controller.buy(
                    code=self.code,
                    signal_date=signal_date,
                    traded_date=traded_date,
                    price=price,
                    save=save
                )

            elif values[day - 1] > sell_thread and values[day] <= sell_thread:
                if day == len(self.candles) - 1:
                    signal_date = self.candles[day].date
                    traded_date = None
                    price = None
                else:
                    signal_date = self.candles[day].date
                    traded_date = self.candles[day + 1].date
                    price = self.candles[day + 1].open

                signal_event_controller.sell(
                    code=self.code,
                    signal_date=signal_date,
                    traded_date=traded_date,
                    price=price,
                    save=save
                )

        return signal_event_controller

    def optimization(self, period_low, period_up,
                     buy_thread_low, buy_thread_up, sell_thread_low, sell_thread_up):
        logger.info(
            '<action=Rsi->>optimization>: Rsi backtest and params optimization Start')

        performance = 0
        best_period = 0
        best_buy_thread = 0
        best_sell_thread = 0

        for period in range(period_low, period_up):
            for buy_thread in range(buy_thread_low, buy_thread_up):
                for sell_thred in range(sell_thread_low, sell_thread_up):
                    signal_event_controller = self.back_test(
                        period=period,
                        buy_thread=buy_thread,
                        sell_thread=sell_thred,
                        backtest=True
                    )
                    if signal_event_controller is None:
                        continue
                    profit = signal_event_controller.profit
                    if performance < profit:
                        performance = profit
                        best_period = period
                        best_buy_thread = buy_thread
                        best_sell_thread = sell_thred

        logger.info(
            '<action=Rsi->>optimization>: Rsi backtest and params optimization End')

        return performance, best_period, best_buy_thread, best_sell_thread


class Macd(object):
    def __init__(self, code, candles, closes):
        self.code = code
        self.candles = candles
        self.closes = closes

    def back_test(self, fast_period, slow_period, signal_period, base=constants.BACKTEST,
                  backtest=False, save=False):
        if len(self.candles) <= fast_period or len(self.candles) <= slow_period or len(self.candles) <= signal_period:
            return None

        signal_event_controller = SignalEventController(base=base)
        if base == constants.MACD and save:
            signal_event_controller.delete(code=self.code)

        macd, macd_signal, _ = talib.MACD(
            np.asarray(self.closes), fast_period, slow_period, signal_period)

        for day in range(1, len(self.candles)):
            if day == len(self.candles) - 1 and backtest:
                continue

            if macd[day - 1] < macd_signal[day - 1] and macd[day] >= macd_signal[day] and \
                    macd[day] < 0 and macd_signal[day] < 0:
                if day == len(self.candles) - 1:
                    signal_date = self.candles[day].date
                    traded_date = None
                    price = None
                else:
                    signal_date = self.candles[day].date
                    traded_date = self.candles[day + 1].date
                    price = self.candles[day + 1].open

                signal_event_controller.buy(
                    code=self.code,
                    signal_date=signal_date,
                    traded_date=traded_date,
                    price=price,
                    save=save
                )

            elif macd[day - 1] > macd_signal[day - 1] and macd[day] <= macd_signal[day] and \
                    macd[day] > 0 and macd_signal[day] > 0:
                if day == len(self.candles) - 1:
                    signal_date = self.candles[day].date
                    traded_date = None
                    price = None
                else:
                    signal_date = self.candles[day].date
                    traded_date = self.candles[day + 1].date
                    price = self.candles[day + 1].open

                signal_event_controller.sell(
                    code=self.code,
                    signal_date=signal_date,
                    traded_date=traded_date,
                    price=price,
                    save=save
                )

        return signal_event_controller

    def optimization(self, fast_period_low, fast_period_up,
                     slow_period_low, slow_period_up, signal_period_low, signal_period_up):
        logger.info(
            '<action=Macd->>optimization>: Macd backtest and params optimization Start')

        performance = 0
        best_fast_period = 0
        best_slow_period = 0
        best_signal_period = 0

        for fast_period in range(fast_period_low, fast_period_up):
            for slow_period in range(slow_period_low, slow_period_up):
                for signal_period in range(signal_period_low, signal_period_up):
                    signal_event_controller = self.back_test(
                        fast_period=fast_period,
                        slow_period=slow_period,
                        signal_period=signal_period,
                        backtest=True
                    )
                    if signal_event_controller is None:
                        continue
                    profit = signal_event_controller.profit
                    if performance < profit:
                        performance = profit
                        best_fast_period = fast_period
                        best_slow_period = slow_period
                        best_signal_period = signal_period

        logger.info(
            '<action=Macd->>optimization>: Macd backtest and params optimization End')

        return performance, best_fast_period, best_slow_period, best_signal_period


class Willr(object):
    def __init__(self, code, candles, highs, lows, closes):
        self.code = code
        self.candles = candles
        self.highs = highs
        self.lows = lows
        self.closes = closes

    def back_test(self, period, buy_thread, sell_thread, base=constants.BACKTEST,
                  backtest=False, save=False):
        if len(self.candles) <= period:
            return None

        signal_event_controller = SignalEventController(base=base)
        if base == constants.WILLR and save:
            signal_event_controller.delete(code=self.code)

        values = talib.WILLR(
            np.asarray(self.highs), np.asarray(self.lows), np.asarray(self.closes))

        for day in range(1, len(self.candles)):
            if values[day - 1] == 0 or values[day - 1] == -100:
                continue
            if day == len(self.candles) - 1 and backtest:
                continue

            if values[day - 1] < buy_thread and values[day] >= buy_thread:
                if day == len(self.candles) - 1:
                    signal_date = self.candles[day].date
                    traded_date = None
                    price = None
                else:
                    signal_date = self.candles[day].date
                    traded_date = self.candles[day + 1].date
                    price = self.candles[day + 1].open

                signal_event_controller.buy(
                    code=self.code,
                    signal_date=signal_date,
                    traded_date=traded_date,
                    price=price,
                    save=save
                )

            elif values[day - 1] > sell_thread and values[day] <= sell_thread:
                if day == len(self.candles) - 1:
                    signal_date = self.candles[day].date
                    traded_date = None
                    price = None
                else:
                    signal_date = self.candles[day].date
                    traded_date = self.candles[day + 1].date
                    price = self.candles[day + 1].open

                signal_event_controller.sell(
                    code=self.code,
                    signal_date=signal_date,
                    traded_date=traded_date,
                    price=price,
                    save=save
                )

        return signal_event_controller

    def optimization(self, period_low, period_up,
                     buy_thread_low, buy_thread_up, sell_thread_low, sell_thread_up):
        logger.info(
            '<action=Willr->>optimization>: Willr backtest and params optimization Start')

        performance = 0
        best_period = 0
        best_buy_thread = 0
        best_sell_thread = 0

        for period in range(period_low, period_up):
            for buy_thread in range(buy_thread_low, buy_thread_up):
                for sell_thred in range(sell_thread_low, sell_thread_up):
                    signal_event_controller = self.back_test(
                        period=period,
                        buy_thread=buy_thread,
                        sell_thread=sell_thred,
                        backtest=True
                    )
                    if signal_event_controller is None:
                        continue
                    profit = signal_event_controller.profit
                    if performance < profit:
                        performance = profit
                        best_period = period
                        best_buy_thread = buy_thread
                        best_sell_thread = sell_thred

        logger.info(
            '<action=Willr->>optimization>: Willr backtest and params optimization End')

        return performance, best_period, best_buy_thread, best_sell_thread


class Stochf(object):
    def __init__(self, code, candles, highs, lows, closes):
        self.code = code
        self.candles = candles
        self.highs = highs
        self.lows = lows
        self.closes = closes

    def back_test(self, fastk_period, fastd_period, buy_thread, sell_thread,
                  base=constants.BACKTEST, backtest=False, save=False):
        if len(self.candles) <= fastk_period or len(self.candles) <= fastd_period:
            return None

        signal_event_controller = SignalEventController(base=base)
        if base == constants.STOCHF and save:
            signal_event_controller.delete(code=self.code)

        fastk, fastd = talib.STOCHF(np.asarray(self.highs), np.asarray(self.lows), np.asarray(self.closes),
                                    fastk_period, fastd_period, 0)

        for day in range(1, len(self.candles)):
            if day == len(self.candles) - 1 and backtest:
                continue

            if fastk[day - 1] < fastd[day - 1] and fastk[day] >= fastd[day] and fastd[day] < buy_thread:
                if day == len(self.candles) - 1:
                    signal_date = self.candles[day].date
                    traded_date = None
                    price = None
                else:
                    signal_date = self.candles[day].date
                    traded_date = self.candles[day + 1].date
                    price = self.candles[day + 1].open

                signal_event_controller.buy(
                    code=self.code,
                    signal_date=signal_date,
                    traded_date=traded_date,
                    price=price,
                    save=save
                )

            elif fastk[day - 1] > fastd[day - 1] and fastk[day] <= fastd[day] and fastd[day] > sell_thread:
                if day == len(self.candles) - 1:
                    signal_date = self.candles[day].date
                    traded_date = None
                    price = None
                else:
                    signal_date = self.candles[day].date
                    traded_date = self.candles[day + 1].date
                    price = self.candles[day + 1].open

                signal_event_controller.sell(
                    code=self.code,
                    signal_date=signal_date,
                    traded_date=traded_date,
                    price=price,
                    save=save
                )

        return signal_event_controller

    def optimization(self, fastk_period_low, fastk_period_up, fastd_period_low, fastd_period_up,
                     buy_thread_low, buy_thread_up, sell_thread_low, sell_thread_up):
        logger.info(
            '<action=Stochf->>optimization>: Stochf backtest and params optimization Start')

        performance = 0
        best_fastk_period = 0
        best_fastd_period = 0
        best_buy_thread = 0
        best_sell_thread = 0

        for fastk_period in range(fastk_period_low, fastk_period_up):
            for fastd_period in range(fastd_period_low, fastd_period_up):
                for buy_thread in range(buy_thread_low, buy_thread_up):
                    for sell_thread in range(sell_thread_low, sell_thread_up):
                        signal_envent_controller = self.back_test(
                            fastk_period=fastk_period,
                            fastd_period=fastd_period,
                            buy_thread=buy_thread,
                            sell_thread=sell_thread,
                            backtest=True
                        )
                        if signal_envent_controller is None:
                            continue
                        profit = signal_envent_controller.profit
                        if performance < profit:
                            performance = profit
                            best_fastk_period = fastk_period
                            best_fastd_period = fastd_period
                            best_buy_thread = buy_thread
                            best_sell_thread = sell_thread

        logger.info(
            '<action=Stochf->optimization>: Stochf backtest and params optimization End')

        return performance, best_fastk_period, best_fastd_period, best_buy_thread, best_sell_thread


class Stoch(object):
    def __init__(self, code, candles, highs, lows, closes):
        self.code = code
        self.candles = candles
        self.highs = highs
        self.lows = lows
        self.closes = closes

    def back_test(self, fastk_period, slowk_period, slowd_period, buy_thread, sell_thread,
                  base=constants.BACKTEST, backtest=False, save=False):
        if len(self.candles) <= fastk_period or len(self.candles) <= slowk_period or len(self.candles) <= slowd_period:
            return None

        signal_event_controller = SignalEventController(base=base)
        if base == constants.STOCH and save:
            signal_event_controller.delete(code=self.code)

        slowk, slowd = talib.STOCH(np.asarray(self.highs), np.asarray(self.lows), np.asarray(self.closes),
                                   fastk_period, slowk_period, 0, slowd_period, 0)

        for day in range(1, len(self.candles)):
            if day == len(self.candles) - 1 and backtest:
                continue

            if slowk[day - 1] < slowd[day - 1] and slowk[day] >= slowd[day] and slowd[day] < buy_thread:
                if day == len(self.candles) - 1:
                    signal_date = self.candles[day].date
                    traded_date = None
                    price = None
                else:
                    signal_date = self.candles[day].date
                    traded_date = self.candles[day + 1].date
                    price = self.candles[day + 1].open

                signal_event_controller.buy(
                    code=self.code,
                    signal_date=signal_date,
                    traded_date=traded_date,
                    price=price,
                    save=save
                )

            elif slowk[day - 1] > slowd[day - 1] and slowk[day] <= slowd[day] and slowd[day] > sell_thread:
                if day == len(self.candles) - 1:
                    signal_date = self.candles[day].date
                    traded_date = None
                    price = None
                else:
                    signal_date = self.candles[day].date
                    traded_date = self.candles[day + 1].date
                    price = self.candles[day + 1].open

                signal_event_controller.sell(
                    code=self.code,
                    signal_date=signal_date,
                    traded_date=traded_date,
                    price=price,
                    save=save
                )

        return signal_event_controller

    def optimization(self, fastk_period_low, fastk_period_up, slowk_period_low, slowk_period_up,
                     slowd_period_low, slowd_period_up, buy_thread_low, buy_thread_up, sell_thread_low, sell_thread_up):
        logger.info(
            '<action=Stoch->optimization>: Stoch backtest and params optimization Start')

        performance = 0
        best_fastk_period = 0
        best_slowk_period = 0
        best_slowd_period = 0
        best_buy_thread = 0
        best_sell_thread = 0

        for fastk_period in range(fastk_period_low, fastk_period_up):
            for slowk_period in range(slowk_period_low, slowk_period_up):
                for slowd_period in range(slowd_period_low, slowd_period_up):
                    for buy_thread in range(buy_thread_low, buy_thread_up):
                        for sell_thread in range(sell_thread_low, sell_thread_up):
                            signal_envent_controller = self.back_test(
                                fastk_period=fastk_period,
                                slowk_period=slowk_period,
                                slowd_period=slowd_period,
                                buy_thread=buy_thread,
                                sell_thread=sell_thread,
                                backtest=True
                            )
                            if signal_envent_controller is None:
                                continue
                            profit = signal_envent_controller.profit
                            if performance < profit:
                                performance = profit
                                best_fastk_period = fastk_period
                                best_slowk_period = slowk_period
                                best_slowd_period = slowd_period
                                best_buy_thread = buy_thread
                                best_sell_thread = sell_thread

        logger.info(
            '<action=Stoch->optimization>: Stoch backtest and params optimization End')

        return performance, best_fastk_period, best_slowk_period, best_slowd_period, best_buy_thread, best_sell_thread
