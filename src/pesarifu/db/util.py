from functools import wraps

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pesarifu.config.constants import CONFIG
from pesarifu.util.helpers import logger

DB_URL = CONFIG["DEV_DB_URL"]
if CONFIG.get("PROD", False):
    DB_URL = CONFIG["DB_URL"]

engine = create_engine(DB_URL)
Session = sessionmaker(engine)


def db_connector(func):
    @wraps(func)
    def with_connection_(*args, **kwargs):
        session = Session()
        try:
            rv = func(session, *args, **kwargs)
        except sqlalchemy.exc.SQLAlchemyError:
            session.rollback()
            logger.error("Database connection error")
            raise
        else:
            session.commit()
        finally:
            session.expunge_all()
            session.close()
        return rv

    return with_connection_
