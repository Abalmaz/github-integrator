import os
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DEBUG = bool(os.environ.get("DEBUG", False))

# Database config
DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]
DB_NAME = os.environ["DB_NAME"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ.get("DB_PORT", 5432)

CLOUD_SQL_CONNECTION = os.environ['CLOUD_SQL_CONNECTION']

if DEBUG:
    DB_CONNECTION_STRING = f"postgresql+pg8000://{DB_USER}:{DB_PASS}@" \
                           f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    DB_CONNECTION_STRING = f"postgresql+pg8000://{DB_USER}:{DB_PASS}@/{DB_NAME}" \
                           f"?unix_sock=/cloudsql/{CLOUD_SQL_CONNECTION}/.s.PGSQL.5432"

engine = sqlalchemy.create_engine(DB_CONNECTION_STRING)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)
