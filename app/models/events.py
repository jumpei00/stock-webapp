import logging
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import desc
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError

import omitempty

from app.models.base import Base
from app.models.base import engine
from app.models.base import session_scope
import constants

logger = logging.getLogger(__name__)


def factory_signalevent_class(base):
    if base == constants.BACKTEST:
        return SignalEventForBackTest
    elif base == constants.EMA:
        return SignalEventForOptimizedEma
    elif base == constants.BBANDS:
        return SignalEventForOptimizedBBands
    elif base == constants.ICHIMOKU:
        return SignalEventForOptimizedIchimoku
    elif base == constants.RSI:
        return SignalEventForOptimizedRsi
    elif base == constants.MACD:
        return SignalEventForOptimizedMacd
    elif base == constants.WILLR:
        return SignalEventForOptimizedWillr
    elif base == constants.STOCHF:
        return SignalEventForOptimizedStochf
    elif base == constants.STOCH:
        return SignalEventForOptimizedStoch


class SignalEventController(object):
    def __init__(self, base, signals=None):
        self.base = factory_signalevent_class(base=base)
        if signals is None:
            self.signals = []
        else:
            self.signals = signals

    def can_buy(self, signal_date):
        if len(self.signals) == 0:
            return True

        last_signal = self.signals[-1]
        if last_signal.side == constants.SELL and last_signal.signal_date < signal_date:
            return True

        return False

    def can_sell(self, signal_date):
        if len(self.signals) == 0:
            return False

        last_signal = self.signals[-1]
        if last_signal.side == constants.BUY and last_signal.signal_date < signal_date:
            return True

        return False

    def buy(self, code, signal_date, traded_date, price, save):
        if not self.can_buy(signal_date=signal_date):
            return False

        signal_event = self.base(
            code=code, signal_date=signal_date, traded_date=traded_date,
            side=constants.BUY, price=price)

        if save:
            signal_event.save()

        self.signals.append(signal_event)
        return True

    def sell(self, code, signal_date, traded_date, price, save):
        if not self.can_sell(signal_date=signal_date):
            return False

        signal_event = self.base(
            code=code, signal_date=signal_date, traded_date=traded_date,
            side=constants.SELL, price=price)

        if save:
            signal_event.save()

        self.signals.append(signal_event)
        return True

    def delete(self, code):
        self.base.delete(code=code)
        return True

    @staticmethod
    def get_signal_events_for_code(base, code):
        signal_events = factory_signalevent_class(
            base=base).get_signal_events_for_code(code=code)
        return SignalEventController(base=base, signals=signal_events)

    @staticmethod
    def get_signal_events_of_recent_day(base, code):
        signal_events = factory_signalevent_class(
            base=base).get_signal_events_for_code(code=code)
        if not signal_events:
            return None
        return signal_events[-1]

    @property
    def profit(self):
        total = constants.TOTAL
        before_sell = constants.BEFORE_SELL
        is_holding = False
        for i in range(len(self.signals)):
            signal_event = self.signals[i]
            if i == 0 and signal_event.side == constants.SELL:
                continue
            if signal_event.price is None:
                continue
            if signal_event.side == constants.BUY:
                total -= signal_event.price
                is_holding = True
            if signal_event.side == constants.SELL:
                total += signal_event.price
                is_holding = False
                before_sell = total
        if is_holding:
            return round(before_sell, 1)
        return round(total, 1)

    @property
    def value(self):
        signals = [s.values for s in self.signals]
        profit = self.profit

        if not signals:
            signals = None

        return {
            'signals': signals,
            'profit': profit
        }


class SignalEventMixnin(object):
    id = Column(Integer, primary_key=True)
    signal_date = Column(DateTime)
    traded_date = Column(DateTime)
    side = Column(String)
    price = Column(Float)

    def save(self):
        with session_scope() as session:
            session.add(self)

    @classmethod
    def get_signal_events_for_code(cls, code):
        with session_scope() as session:
            signal_events = session.query(cls).filter(
                cls.code == code).order_by(
                    desc(cls.signal_date)).all()
            if signal_events is None:
                return []
            signal_events.reverse()
            return signal_events

    @classmethod
    def delete(cls, code):
        with session_scope() as session:
            latest_event = session.query(cls).filter(cls.code == code).all()
            if latest_event is None:
                return True
            for event in latest_event:
                session.delete(event)
        return True

    @property
    def values(self):
        dict_values = omitempty({
            'code': self.code,
            'signal_date': self.signal_date,
            'traded_date': self.traded_date,
            'side': self.side,
            'price': self.price
        })
        if not dict_values:
            return None
        return dict_values


class SignalEventForBackTest(SignalEventMixnin, Base):
    __tablename__ = 'backtest_signal_event'
    code = Column(String)


class SignalEventForOptimizedEma(SignalEventMixnin, Base):
    __tablename__ = 'ema_signal_event'
    code = Column(String, ForeignKey('latest_backtest_results.code'))
    _ema = relationship('LatestBackTestResults', back_populates='ema')


class SignalEventForOptimizedBBands(SignalEventMixnin, Base):
    __tablename__ = 'bb_signal_event'
    code = Column(String, ForeignKey('latest_backtest_results.code'))
    _bb = relationship('LatestBackTestResults', back_populates='bb')


class SignalEventForOptimizedIchimoku(SignalEventMixnin, Base):
    __tablename__ = 'ichimoku_signal_event'
    code = Column(String, ForeignKey('latest_backtest_results.code'))
    _ichimoku = relationship('LatestBackTestResults',
                             back_populates='ichimoku')


class SignalEventForOptimizedRsi(SignalEventMixnin, Base):
    __tablename__ = 'rsi_signal_event'
    code = Column(String, ForeignKey('latest_backtest_results.code'))
    _rsi = relationship('LatestBackTestResults', back_populates='rsi')


class SignalEventForOptimizedMacd(SignalEventMixnin, Base):
    __tablename__ = 'macd_signal_event'
    code = Column(String, ForeignKey('latest_backtest_results.code'))
    _macd = relationship('LatestBackTestResults', back_populates='macd')


class SignalEventForOptimizedWillr(SignalEventMixnin, Base):
    __tablename__ = 'willr_signal_event'
    code = Column(String, ForeignKey('latest_backtest_results.code'))
    _willr = relationship('LatestBackTestResults', back_populates='willr')


class SignalEventForOptimizedStochf(SignalEventMixnin, Base):
    __tablename__ = 'stochf_signal_event'
    code = Column(String, ForeignKey('latest_backtest_results.code'))
    _stochf = relationship('LatestBackTestResults', back_populates='stochf')


class SignalEventForOptimizedStoch(SignalEventMixnin, Base):
    __tablename__ = 'stoch_signal_event'
    code = Column(String, ForeignKey('latest_backtest_results.code'))
    _stoch = relationship('LatestBackTestResults', back_populates='stoch')


class BackTestParamsController(object):
    def __init__(self, code, params=None):
        self.code = code
        if params is None:
            self.params = []
        else:
            self.params = params

    def create_params(self, df_params):
        LatestBackTestResults.delete(code=self.code)
        LatestBackTestResults.create_params(
            code=self.code, df_params=df_params)

    @property
    def get_params(self):
        params = LatestBackTestResults.get_params(code=self.code)
        return BackTestParamsController(code=self.code, params=params)

    @property
    def value(self):
        if not self.params:
            params = None
        else:
            params = self.params.values

        return params


class LatestBackTestResults(Base):
    __tablename__ = 'latest_backtest_results'

    date = Column(DateTime, primary_key=True)
    code = Column(String)
    ema = relationship('SignalEventForOptimizedEma',
                       back_populates='_ema', cascade='all, delete')
    bb = relationship('SignalEventForOptimizedBBands',
                      back_populates='_bb', cascade='all, delete')
    ichimoku = relationship('SignalEventForOptimizedIchimoku',
                            back_populates='_ichimoku', cascade='all, delete')
    rsi = relationship('SignalEventForOptimizedRsi',
                       back_populates='_rsi', cascade='all, delete')
    macd = relationship('SignalEventForOptimizedMacd',
                        back_populates='_macd', cascade='all, delete')
    willr = relationship('SignalEventForOptimizedWillr',
                         back_populates='_willr', cascade='all, delete')
    stochf = relationship('SignalEventForOptimizedStochf',
                          back_populates='_stochf', cascade='all, delete')
    stoch = relationship('SignalEventForOptimizedStoch',
                         back_populates='_stoch', cascade='all, delete')
    ema_performance = Column(Float)
    ema_short_period = Column(Integer)
    ema_long_period = Column(Integer)
    bb_performance = Column(Float)
    bb_n = Column(Integer)
    bb_k = Column(Float)
    ichimoku_performance = Column(Float)
    rsi_performance = Column(Float)
    rsi_period = Column(Integer)
    rsi_buy_thread = Column(Float)
    rsi_sell_thread = Column(Float)
    macd_performance = Column(Float)
    macd_fast_period = Column(Integer)
    macd_slow_period = Column(Integer)
    macd_signal_period = Column(Integer)
    willr_performance = Column(Float)
    willr_period = Column(Integer)
    willr_buy_thread = Column(Float)
    willr_sell_thread = Column(Float)
    stochf_performance = Column(Float)
    stochf_fastk_period = Column(Integer)
    stochf_fastd_period = Column(Integer)
    stochf_buy_thread = Column(Float)
    stochf_sell_thread = Column(Float)
    stoch_performance = Column(Float)
    stoch_fastk_period = Column(Integer)
    stoch_slowk_period = Column(Integer)
    stoch_slowd_period = Column(Integer)
    stoch_buy_thread = Column(Float)
    stoch_sell_thread = Column(Float)

    @classmethod
    def create_params(cls, code, df_params):
        try:
            df_params.to_sql(cls.__tablename__, con=engine,
                             index_label='date', if_exists='append')
        except IntegrityError as ie:
            logger.warning(
                '<action=LatestBackTestResults->>create_params>: {}'.format(ie))
            raise
        return True

    @classmethod
    def get_params(cls, code):
        with session_scope() as session:
            params = session.query(cls).filter(cls.code == code).first()
        if params is None:
            return []
        return params

    @classmethod
    def delete(cls, code):
        with session_scope() as session:
            latest_params = session.query(cls).filter(cls.code == code).first()
            if latest_params is None:
                return True
            session.delete(latest_params)
        return True

    @property
    def values(self):
        dict_values = omitempty({
            'date': self.date,
            'code': self.code,
            'ema_performance': self.ema_performance,
            'ema_short_period': self.ema_short_period,
            'ema_long_period': self.ema_long_period,
            'bb_performance': self.bb_performance,
            'bb_n': self.bb_n,
            'bb_k': self.bb_k,
            'ichimoku_performance': self.ichimoku_performance,
            'rsi_performance': self.rsi_performance,
            'rsi_period': self.rsi_period,
            'rsi_buy_thread': self.rsi_buy_thread,
            'rsi_sell_thread': self.rsi_sell_thread,
            'macd_performance': self.macd_performance,
            'macd_fast_period': self.macd_fast_period,
            'macd_slow_period': self.macd_slow_period,
            'macd_signal_period': self.macd_signal_period,
            'willr_performance': self.willr_performance,
            'willr_period': self.willr_period,
            'willr_buy_thread': self.willr_buy_thread,
            'willr_sell_thread': self.willr_sell_thread,
            'stochf_performance': self.stochf_performance,
            'stochf_fastk_period': self.stochf_fastk_period,
            'stochf_fastd_period': self.stochf_fastd_period,
            'stochf_buy_thread': self.stochf_buy_thread,
            'stochf_sell_thread': self.stochf_sell_thread,
            'stoch_performance': self.stoch_performance,
            'stoch_fastk_period': self.stoch_fastk_period,
            'stoch_slowk_period': self.stoch_slowk_period,
            'stoch_slowd_period': self.stoch_slowd_period,
            'stoch_buy_thread': self.stoch_buy_thread,
            'stoch_sell_thread': self.stoch_sell_thread})
        if not dict_values:
            return None
        return dict_values
