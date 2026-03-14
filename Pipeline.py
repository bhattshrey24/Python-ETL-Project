
import asyncio

from Ingestion import ingest_data

async def main() :
    await ingest_data() # creates event loop