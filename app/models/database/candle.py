import logging

from sqlalchemy import Column
from sqlalchemy import desc
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy.types import Float as Float_type
from sqlalchemy.exc import IntegrityError

from app.models.database.base import Base
from app.models.database.base import engine
from app.models.database.base import session_scope


logger = logging.getLogger(__name__)


class StockData(Base):
    __tablename__ = 'candle_data'
    date = Column(DateTime, primary_key=True, nullable=False)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)

    @property
    def values(self):
        return {
            'date': self.date,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close}

    @classmethod
    def create(cls, stock_df):
        stock_df.rename(columns=str.lower, inplace=True)
        try:
            stock_df.to_sql(cls.__tablename__, con=engine, index_label='date',
                            if_exists='replace', dtype=Float_type())
            return True
        except IntegrityError:
            return False

    @classmethod
    def get(cls, date):
        with session_scope() as session:
            candle = session.query(cls).filter(cls.date == date).first()
        if candle is None:
            return None
        return candle

    @classmethod
    def get_all_candles(cls, limit=100):
        with session_scope() as session:
            candles = session.query(cls).limit(limit).all()
        if candles is None:
            return None
        return candles
