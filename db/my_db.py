import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from config.db_constants import MY_DB
import threading
import streamlit as st

username   = st.secrets["mysql"]["username"]
password   = quote_plus(st.secrets["mysql"]["password"]) # asdasd@24 → asdasd%4024 and mysql knows %40 means @
host       = st.secrets["mysql"]["host"]
port       = int(st.secrets["mysql"]["port"])  #  MySQL expects port as Int
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
    with _engine_lock: # stops 2 or more threads from creating the engine again
        if db_engine is None:
            db_engine = create_engine(
                f"mysql+pymysql://{username}:{password}@{host}:{port}/{db}",
                pool_pre_ping=True,
                pool_timeout=30,      # wait up to 30s for a free connection
                pool_recycle=1800,    # recycle connections every 30 mins
                                      # prevents MySQL's 8hr timeout from killing them
                connect_args={"connect_timeout": 10}
            )
    return db_engine

Base = declarative_base()  # Its just a base class that all ORM models inherit from.
