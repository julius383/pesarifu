from functools import wraps

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pesarifu.config.config import settings
from pesarifu.util.helpers import logger

engine = create_engine(settings.DB_URL)
Session = sessionmaker(engine)


def db_connector(func):
    @wraps(func)
    def with_connection_(*args, **kwargs):
        session = Session()
        try:
            rv = func(session, *args, **kwargs)
        except sqlalchemy.exc.SQLAlchemyError:
            session.rollback()
            logger.exception("Database connection error")
            raise
        else:
            session.commit()
        finally:
            session.expunge_all()
            session.close()
        return rv

    return with_connection_
