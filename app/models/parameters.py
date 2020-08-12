from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

from app.models.base import Base
from app.models.base import session_scope


class LatestBackTestResults(Base):
    __tablename__ = 'latest_backtest_results'

    id = Column(Integer, primary_key=True)
    code = Column(String)
    date = Column(DateTime)
    ema_ranking = Column(Integer)
    ema_performance = Column(Float)
    ema_short_period = Column(Integer)
    ema_long_period = Column(Integer)
    bb_ranking = Column(Integer)
    bb_performance = Column(Float)
    bb_n = Column(Integer)
    bb_k = Column(Float)
    ichimoku_ranking = Column(Integer)
    ichimoku_performance = Column(Float)
    rsi_ranking = Column(Integer)
    rsi_performance = Column(Float)
    rsi_period = Column(Integer)
    rsi_buy_thread = Column(Float)
    rsi_sell_thread = Column(Float)
    macd_ranking = Column(Integer)
    macd_performance = Column(Float)
    macd_fast_period = Column(Integer)
    macd_slow_period = Column(Integer)
    macd_signal_period = Column(Integer)
    willr_ranking = Column(Integer)
    willr_performance = Column(Float)
    willr_period = Column(Integer)
    willr_buy_thread = Column(Float)
    willr_sell_thread = Column(Float)
    stochf_ranking = Column(Integer)
    stochf_performance = Column(Float)
    stochf_fastk_period = Column(Integer)
    stochf_fastd_period = Column(Integer)
    stochf_buy_thread = Column(Float)
    stochf_sell_thread = Column(Float)
    stoch_ranking = Column(Integer)
    stoch_performance = Column(Float)
    stoch_fastk_period = Column(Integer)
    stoch_slowk_period = Column(Integer)
    stoch_slowd_period = Column(Integer)
    stoch_buy_thread = Column(Float)
    stoch_sell_thread = Column(Float)
