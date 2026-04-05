
import asyncio

from ingestion.ingestion import ingest_data
from transformation.transformation import transform_data

async def main() :
#   await ingest_data() # creates event loop
    await transform_data() # creates event loop