import sqlalchemy
from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from pesarifu.util.helpers import logger

config = dotenv_values(".env")
engine = create_engine(config["DB_URL"])


def db_connector(func):
    def with_connection_(*args, **kwargs):
        session = Session(engine)
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
