from contextlib import contextmanager
import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

import settings


logger = logging.getLogger(__name__)
Base = declarative_base()
engine = create_engine(f'sqlite:///{settings.db_name}')
Session = scoped_session(sessionmaker(bind=engine))


@contextmanager
def session_scope():
    session = Session()
    session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except Exception as e:
        logger.error(f'action=session_scope error={e}')
        session.rollback()
        raise
    finally:
        session.expire_on_commit = True


def init_db():
    import app.models.events  # noqa: F401
    Base.metadata.create_all(bind=engine)
