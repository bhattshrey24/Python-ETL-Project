import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base
from config.db_constants import MY_DB
import threading

load_dotenv()

username = os.getenv("MY_SQL_USERNAME")
password = quote_plus(os.getenv("MY_SQL_PASSWORD"))
host = os.getenv("MY_SQL_HOST")
port = os.getenv("MY_SQL_PORT")
db = MY_DB

# Using singleton pattern, so that we don't create multiple connections to db everytime we want to access it
app_engine = None
db_engine = None

_engine_lock = threading.Lock() # Since db_engine is a module-level global, if two coroutines
# both check if db_engine is None at the same time before either has set it, you'll
# create two engines


def get_app_engine():
    global app_engine  # Accessing global "app_engine" otherwise it would have created local variable instead of using global one

    if app_engine is None:
        app_engine = create_engine(
            f"mysql+pymysql://{username}:{password}@{host}:{port}",
            pool_pre_ping=True,
            pool_timeout=10,
            connect_args={"connect_timeout": 10}
        )

    return app_engine


def get_db_engine():
    global db_engine

    with _engine_lock:
        if db_engine is None:
            db_engine = create_engine(
                f"mysql+pymysql://{username}:{password}@{host}:{port}/{db}",
                pool_pre_ping=True,
                pool_timeout=10,
                connect_args={"connect_timeout": 10}
            )

    return db_engine


Base = declarative_base()  # Its just a base class that all ORM models inherit from.
