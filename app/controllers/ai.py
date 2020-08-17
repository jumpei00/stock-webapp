from datetime import datetime
import pandas as pd
import logging

from dict2obj import Dict2Obj

from app.models.dfcandles import DataFrameCandle
from app.technical.backtest import BackTestingSerializer
from app.models.events import SignalEventController
import constants

logger = logging.getLogger(__name__)


class AI(object):
    def __init__(self, code):
        self.code = code
        self.df = DataFrameCandle(code=self.code)
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

        ema_performance, \
            ema_short_period, \
            ema_long_period = \
            self.backtest_serializer.ema.optimization(
                short_period_low=test_params_ema.ema1, short_period_up=test_params_ema.ema2,
                long_period_low=test_params_ema.ema3, long_period_up=test_params_ema.ema4
            )

        bb_performance, \
            bb_n, \
            bb_k = \
            self.backtest_serializer.bbands.optimization(
                n_low=test_params_bb.bb1, n_up=test_params_bb.bb2,
                k_low=test_params_bb.bb3, k_up=test_params_bb.bb4
            )

        ichimoku_performance = \
            self.backtest_serializer.ichimoku.optimization()

        rsi_performance, \
            rsi_period, \
            rsi_buy_thread, \
            rsi_sell_thread = \
            self.backtest_serializer.rsi.optimization(
                period_low=test_params_rsi.rsi1, period_up=test_params_rsi.rsi2,
                buy_thread_low=test_params_rsi.rsi3, buy_thread_up=test_params_rsi.rsi4,
                sell_thread_low=test_params_rsi.rsi5, sell_thread_up=test_params_rsi.rsi6
            )

        macd_performance, \
            macd_fast_period, \
            macd_slow_period, \
            macd_signal_period = \
            self.backtest_serializer.macd.optimization(
                fast_period_low=test_params_macd.macd1, fast_period_up=test_params_macd.macd2,
                slow_period_low=test_params_macd.macd3, slow_period_up=test_params_macd.macd4,
                signal_period_low=test_params_macd.macd5, signal_period_up=test_params_macd.macd6
            )

        willr_performance, \
            willr_period, \
            willr_buy_thread, \
            willr_sell_thread = \
            self.backtest_serializer.willr.optimization(
                period_low=test_params_willr.willr1, period_up=test_params_willr.willr2,
                buy_thread_low=test_params_willr.willr3, buy_thread_up=test_params_willr.willr4,
                sell_thread_low=test_params_willr.willr5, sell_thread_up=test_params_willr.willr6
            )

        stochf_performance, \
            stochf_fastk_period, \
            stochf_fastd_period, \
            stochf_buy_thread, \
            stochf_sell_thread = \
            self.backtest_serializer.stochf.optimization(
                fastk_period_low=test_params_stochf.stochf1, fastk_period_up=test_params_stochf.stochf2,
                fastd_period_low=test_params_stochf.stochf3, fastd_period_up=test_params_stochf.stochf4,
                buy_thread_low=test_params_stochf.stochf5, buy_thread_up=test_params_stochf.stochf6,
                sell_thread_low=test_params_stochf.stochf7, sell_thread_up=test_params_stochf.stochf8
            )

        stoch_performance, \
            stoch_fastk_period, \
            stoch_slowk_period, \
            stoch_slowd_period, \
            stoch_buy_thread, \
            stoch_sell_thread = \
            self.backtest_serializer.stoch.optimization(
                fastk_period_low=test_params_stoch.stoch1, fastk_period_up=test_params_stoch.stoch2,
                slowk_period_low=test_params_stoch.stoch3, slowk_period_up=test_params_stoch.stoch4,
                slowd_period_low=test_params_stoch.stoch5, slowd_period_up=test_params_stoch.stoch6,
                buy_thread_low=test_params_stoch.stoch7, buy_thread_up=test_params_stoch.stoch8,
                sell_thread_low=test_params_stoch.stoch9, sell_thread_up=test_params_stoch.stoch10
            )

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
