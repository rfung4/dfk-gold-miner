import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_db_connection_string() -> str:
    if os.name == 'nt':
        return "postgresql://user:password@127.0.0.1:5432/postgres"
    else:
        return "postgresql://user:password@postgres:5432/postgres"


dfkBase = declarative_base()
dfk_engine = create_engine(get_db_connection_string(), pool_recycle=3600)
dfk_session_creator = sessionmaker(dfk_engine)
