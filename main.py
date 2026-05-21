
import asyncio
from pipeline import main
import logging


logging.basicConfig(
    level=logging.DEBUG,                  # change to DEBUG to see raw API responses & SQL data
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


if __name__ == '__main__':
    asyncio.run(main())
