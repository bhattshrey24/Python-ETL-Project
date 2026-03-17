import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base
from config.db_constants import MY_DB

load_dotenv()

username = os.getenv("MY_SQL_USERNAME")
password = quote_plus(os.getenv("MY_SQL_PASSWORD"))
host = os.getenv("MY_SQL_HOST")
port = os.getenv("MY_SQL_PORT")
db = MY_DB

# Using singleton pattern, so that we don't create multiple connections to db everytime we want to access it
app_engine = None
db_engine = None

def get_app_engine():
    global app_engine # Accessing global "app_engine" otherwise it would have created local variable instead of using global one

    if app_engine is None:
        app_engine = create_engine(
            f"mysql+pymysql://{username}:{password}@{host}:{port}"
        )

    return app_engine


def get_db_engine():
    global db_engine

    if db_engine is None:
        db_engine = create_engine(
            f"mysql+pymysql://{username}:{password}@{host}:{port}/{db}"
        )

    return db_engine

Base = declarative_base() # Its just a base class that all ORM models inherit from.