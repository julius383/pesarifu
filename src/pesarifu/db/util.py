from functools import wraps

import sqlalchemy
from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pesarifu.util.helpers import logger

config = dotenv_values()
db_url = config["DEV_DB_URL"]
if config.get("PROD", False):
    db_url = config["DB_URL"]

engine = create_engine(db_url)
Session = sessionmaker(engine)


def db_connector(func):
    @wraps(
        func,
        assigned=(
            "__module__",
            "__name__",
            "__qualname__",
            "__annotations__",
            "__doc__",
            "__code__",
        ),
    )
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
