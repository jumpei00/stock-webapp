from datetime import datetime
from multiprocessing import Pool
from multiprocessing import cpu_count
import pandas as pd
import logging

from dict2obj import Dict2Obj

from app.models.dfcandles import DataFrameCandle
from app.technical.backtest import BackTestingSerializer
from app.models.events import SignalEventController
import constants
import settings

logger = logging.getLogger(__name__)


class AI(object):
    def __init__(self, code):
        self.code = code
        self.cpu_count_num = cpu_count()
        self.df = DataFrameCandle(code=self.code, duration=settings.duration_backtest)
        self.back_test_params = self.df.back_test_params.get_params
        self.backtest_serializer = BackTestingSerializer(
            code=self.code, candles=self.df.candles,
            highs=self.df.highs, lows=self.df.lows, closes=self.df.closes)

    @property
    def set_latest_params(self):
        self.back_test_params = self.df.back_test_params.get_params
        return True

    def trade(self, test_params=None, backtest=False):
        if backtest:
            self.optimize_params(
                test_params_ema=test_params.ema,
                test_params_bb=test_params.bb,
                test_params_rsi=test_params.rsi,
                test_params_macd=test_params.macd,
                test_params_willr=test_params.willr,
                test_params_stochf=test_params.stochf,
                test_params_stoch=test_params.stoch)
            self.set_latest_params

        latest_params = self.back_test_params.value

        if latest_params is None:
            return None

        latest_params = Dict2Obj(latest_params)

        _ = self.backtest_serializer.ema.back_test(
            short_period=latest_params.ema_short_period,
            long_period=latest_params.ema_long_period,
            base=constants.EMA, save=True)

        _ = self.backtest_serializer.bbands.back_test(
            n=latest_params.bb_n, k=latest_params.bb_k,
            base=constants.BBANDS, save=True)

        _ = self.backtest_serializer.ichimoku.back_test(
            base=constants.ICHIMOKU, save=True)

        _ = self.backtest_serializer.rsi.back_test(
            period=latest_params.rsi_period,
            buy_thread=latest_params.rsi_buy_thread,
            sell_thread=latest_params.rsi_sell_thread,
            base=constants.RSI, save=True)

        _ = self.backtest_serializer.macd.back_test(
            fast_period=latest_params.macd_fast_period,
            slow_period=latest_params.macd_slow_period,
            signal_period=latest_params.macd_signal_period,
            base=constants.MACD, save=True)

        _ = self.backtest_serializer.willr.back_test(
            period=latest_params.willr_period,
            buy_thread=latest_params.willr_buy_thread,
            sell_thread=latest_params.willr_sell_thread,
            base=constants.WILLR, save=True)

        _ = self.backtest_serializer.stochf.back_test(
            fastk_period=latest_params.stochf_fastk_period,
            fastd_period=latest_params.stochf_fastd_period,
            buy_thread=latest_params.stochf_buy_thread,
            sell_thread=latest_params.stochf_sell_thread,
            base=constants.STOCHF, save=True)

        _ = self.backtest_serializer.stoch.back_test(
            fastk_period=latest_params.stoch_fastk_period,
            slowk_period=latest_params.stoch_slowk_period,
            slowd_period=latest_params.stoch_slowd_period,
            buy_thread=latest_params.stoch_buy_thread,
            sell_thread=latest_params.stoch_sell_thread,
            base=constants.STOCH, save=True)

        today_trades = self.today_trade()

        return today_trades

    def today_trade(self):
        today_trades = constants.TODAY_TRADES.copy()
        base_list = constants.BASE_LIST
        latest_candle = self.df.candles[-1]

        for today_trades_key, base in zip(today_trades, base_list):
            recent_day_signal_event = SignalEventController.get_signal_events_of_recent_day(
                base=base, code=self.code)
            if recent_day_signal_event is None:
                continue
            if recent_day_signal_event.signal_date == latest_candle.date:
                today_trades[today_trades_key] = recent_day_signal_event.side

        return today_trades

    def optimize_params(self, test_params_ema, test_params_bb, test_params_rsi,
                        test_params_macd, test_params_willr, test_params_stochf, test_params_stoch):
        # multiprocessing
        with Pool(self.cpu_count_num) as pool:

            stoch_pool = pool.apply_async(
                self.backtest_serializer.stoch.optimization,
                (test_params_stoch.stoch1, test_params_stoch.stoch2,
                 test_params_stoch.stoch3, test_params_stoch.stoch4,
                 test_params_stoch.stoch5, test_params_stoch.stoch6,
                 test_params_stoch.stoch7, test_params_stoch.stoch8,
                 test_params_stoch.stoch9, test_params_stoch.stoch10,))

            stochf_pool = pool.apply_async(
                self.backtest_serializer.stochf.optimization,
                (test_params_stochf.stochf1, test_params_stochf.stochf2,
                 test_params_stochf.stochf3, test_params_stochf.stochf4,
                 test_params_stochf.stochf5, test_params_stochf.stochf6,
                 test_params_stochf.stochf7, test_params_stochf.stochf8,))

            macd_pool = pool.apply_async(
                self.backtest_serializer.macd.optimization,
                (test_params_macd.macd1, test_params_macd.macd2,
                 test_params_macd.macd3, test_params_macd.macd4,
                 test_params_macd.macd5, test_params_macd.macd6,))

            rsi_pool = pool.apply_async(
                self.backtest_serializer.rsi.optimization,
                (test_params_rsi.rsi1, test_params_rsi.rsi2,
                 test_params_rsi.rsi3, test_params_rsi.rsi4,
                 test_params_rsi.rsi5, test_params_rsi.rsi6, ))

            willr_pool = pool.apply_async(
                self.backtest_serializer.willr.optimization,
                (test_params_willr.willr1, test_params_willr.willr2,
                 test_params_willr.willr3, test_params_willr.willr4,
                 test_params_willr.willr5, test_params_willr.willr6,))

            bb_pool = pool.apply_async(
                self.backtest_serializer.bbands.optimization,
                (test_params_bb.bb1, test_params_bb.bb2,
                 test_params_bb.bb3, test_params_bb.bb4, ))

            ema_pool = pool.apply_async(
                self.backtest_serializer.ema.optimization,
                (test_params_ema.ema1, test_params_ema.ema2,
                 test_params_ema.ema3, test_params_ema.ema4, ))

            ichimoku_pool = pool.apply_async(
                self.backtest_serializer.ichimoku.optimization)

            stoch_performance, stoch_fastk_period, stoch_slowk_period, stoch_slowd_period, stoch_buy_thread, stoch_sell_thread = stoch_pool.get()
            stochf_performance, stochf_fastk_period, stochf_fastd_period, stochf_buy_thread, stochf_sell_thread = stochf_pool.get()
            macd_performance, macd_fast_period, macd_slow_period, macd_signal_period = macd_pool.get()
            rsi_performance, rsi_period, rsi_buy_thread, rsi_sell_thread = rsi_pool.get()
            willr_performance, willr_period, willr_buy_thread, willr_sell_thread = willr_pool.get()
            bb_performance, bb_n, bb_k = bb_pool.get()
            ema_performance, ema_short_period, ema_long_period = ema_pool.get()
            ichimoku_performance = ichimoku_pool.get()

        backtesting_time = datetime.now()
        optimize_params_list = [self.code,
                                ema_performance, ema_short_period, ema_long_period,
                                bb_performance, bb_n, bb_k,
                                ichimoku_performance,
                                rsi_performance, rsi_period, rsi_buy_thread, rsi_sell_thread,
                                macd_performance, macd_fast_period, macd_slow_period, macd_signal_period,
                                willr_performance, willr_period, willr_buy_thread, willr_sell_thread,
                                stochf_performance, stochf_fastk_period, stochf_fastd_period,
                                stochf_buy_thread, stochf_sell_thread,
                                stoch_performance, stoch_fastk_period, stoch_slowk_period, stoch_slowd_period,
                                stoch_buy_thread, stoch_sell_thread]

        df_params = pd.DataFrame(data=optimize_params_list).T
        df_params.index = [backtesting_time]
        df_params.columns = constants.PARAMS_COL_NAMES

        self.df.back_test_params.create_params(df_params=df_params)

        return True
