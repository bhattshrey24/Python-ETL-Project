
from Ingestion import ingest_data
import asyncio
from Pipeline import main
from config import BASE_URL # Can even import just variables

if __name__ == '__main__':
    asyncio.run(main())
