
import asyncio
from sqlalchemy import text
from db.my_db import *

from ingestion.ingestion import ingest_data
from transformation.transformation import transform_data
from serving.serving import serve_data
async def main() :
      loop = asyncio.get_running_loop()
      await loop.run_in_executor(None, create_db)  # run once at start

      await ingest_data() # creates event loop
      await transform_data() # creates event loop
      await serve_data()


# Responsibility : create database if not exist
def create_db():
    engine = get_app_engine()
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db}"))
        conn.commit()
        print("Database created")

