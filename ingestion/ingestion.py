from functools import partial

import asyncio
import aiohttp
import logging

from sqlalchemy import text

from config.app_constants import *
from datetime import datetime, timezone, date
from config.db_constants import INGESTION_TIMESERIES_TABLE, \
    INGESTION_OVERVIEW_TABLE  # I guess this triggers registering of these ORM classes to Base
from db.my_db import *
from ingestion.models import *

import streamlit as st

api_key  = st.secrets["api"]["key"]
MY_DB = st.secrets["mysql"]["my_db"]

# Set up module-level logger
# Using __name__ ensures the logger is named "ingestion.ingestion" — useful for filtering logs by module
logger = logging.getLogger(__name__)

# ingestion.py
async def ingest_data():
    logger.info("Starting ingestion layer")
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, create_table)

    logger.info("Fetching TIME_SERIES_DAILY from API")
    timeseries_response = await ingest_from_api("TIME_SERIES_DAILY")

    logger.info("Fetching OVERVIEW from API")
    overview_response = await ingest_from_api("OVERVIEW")

    timeseries_data = change_structure(timeseries_response, "timeseries")
    overview_data = change_structure(overview_response, "overview")

    await loop.run_in_executor(None, partial(load_data, timeseries_data, "timeseries"))
    await loop.run_in_executor(None, partial(load_data, overview_data, "overview"))

    logger.info("Ingestion layer completed successfully")


# Responsibility : To call api with required parameters for all symbols and aggregate the result
async def ingest_from_api(function):
    results = []
    for company in COMPANIES: # Coroutine created and awaited in same iteration — never orphaned
        logger.debug(f"Calling API for {company['symbol']} | function={function}")
        result = await ingest_data_for_symbol(
            symbol=company['symbol'], function=function
        )
        results.append(result)
        await asyncio.sleep(1)
    return results



class RateLimitError(Exception):
    """Raised when Alpha Vantage API rate limit is hit."""
    pass

# Responsibility : To call api and get result for single symbol
async def ingest_data_for_symbol(symbol, function):
    await asyncio.sleep(1)
    url = f"{BASE_URL}query?function={function}&symbol={symbol}&apikey={api_key}"

    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as response:
            data = await response.json()

            # Alpha Vantage signals rate limit via these keys
            if "Information" in data or "Note" in data:
                rate_limit_msg = data.get("Information") or data.get("Note")
                logger.error(f"Rate limit hit for {symbol}/{function}: {rate_limit_msg}")
                raise RateLimitError(rate_limit_msg)
            return data



# Responsibility : To change the json response into the required table structure
def change_structure(response, api_type):
    if api_type == "timeseries":
        data = change_structure_for_timeseries(response)
    else:
        data = change_structure_for_overview(response)
    return data


# Responsibility : To change structure for overview response into the required table structure
def change_structure_for_timeseries(response):
    # debug level — full API responses are verbose, only useful when actively debugging
    logger.debug(f"Raw timeseries response: {response}")
    cleaned_data = []  # list of dictionaries where each row is a dictionary
    for data in response:
        meta = data.get("Meta Data",{})  # if key "Meta Data" is not present then this will return empty dictionary instead of None
        tz = clean(meta.get("5. Time Zone"), str)
        symbol = clean(meta.get("2. Symbol"), str)
        timeseries = data.get("Time Series (Daily)", {})
        for dt, values in timeseries.items():  # looping each item in list which is basically stock details of each symbol
            row = {
                "symbol": symbol,
                # "ingestion_date": datetime.now(timezone.utc),
                "timezone": tz,
                "date": clean(dt, date),
                "open": clean(values.get("1. open"), float),
                "high": clean(values.get("2. high"), float),
                "low": clean(values.get("3. low"), float),
                "close": clean(values.get("4. close"), float),
                "volume": clean(values.get("5. volume"), int)
            }

            cleaned_data.append(row)

    logger.info(f"Structured {len(cleaned_data)} timeseries rows")
    return cleaned_data


# Responsibility : To change structure for overview response into the required table structure
def change_structure_for_overview(response):
    logger.debug(f"Raw overview response: {response}")
    cleaned_data = []

    for data in response:
        row = {
            "symbol": clean(data.get("Symbol"), str),
            # "ingestion_date": datetime.now(timezone.utc),

            "asset_type": clean(data.get("AssetType"), str),
            "name": clean(data.get("Name"), str),
            "description": clean(data.get("Description"), str),
            "cik": clean(data.get("CIK"), str),
            "exchange": clean(data.get("Exchange"), str),
            "currency": clean(data.get("Currency"), str),
            "country": clean(data.get("Country"), str),
            "sector": clean(data.get("Sector"), str),
            "industry": clean(data.get("Industry"), str),
            "address": clean(data.get("Address"), str),
            "official_site": clean(data.get("OfficialSite"), str),

            "fiscal_year_end": clean(data.get("FiscalYearEnd"), str),
            "latest_quarter": clean(data.get("LatestQuarter"), date),

            "market_capitalization": clean(data.get("MarketCapitalization"), int),
            "ebitda": clean(data.get("EBITDA"), int),
            "pe_ratio": clean(data.get("PERatio"), float),
            "peg_ratio": clean(data.get("PEGRatio"), float),
            "book_value": clean(data.get("BookValue"), float),
            "dividend_per_share": clean(data.get("DividendPerShare"), float),
            "dividend_yield": clean(data.get("DividendYield"), float),
            "eps": clean(data.get("EPS"), float),
            "revenue_per_share_ttm": clean(data.get("RevenuePerShareTTM"), float),
            "profit_margin": clean(data.get("ProfitMargin"), float),
            "operating_margin_ttm": clean(data.get("OperatingMarginTTM"), float),
            "return_on_assets_ttm": clean(data.get("ReturnOnAssetsTTM"), float),
            "return_on_equity_ttm": clean(data.get("ReturnOnEquityTTM"), float),
            "revenue_ttm": clean(data.get("RevenueTTM"), int),
            "gross_profit_ttm": clean(data.get("GrossProfitTTM"), int),
            "diluted_eps_ttm": clean(data.get("DilutedEPSTTM"), float),

            "quarterly_earnings_growth_yoy": clean(data.get("QuarterlyEarningsGrowthYOY"), float),
            "quarterly_revenue_growth_yoy": clean(data.get("QuarterlyRevenueGrowthYOY"), float),

            "analyst_target_price": clean(data.get("AnalystTargetPrice"), float),
            "analyst_rating_strong_buy": clean(data.get("AnalystRatingStrongBuy"), int),
            "analyst_rating_buy": clean(data.get("AnalystRatingBuy"), int),
            "analyst_rating_hold": clean(data.get("AnalystRatingHold"), int),
            "analyst_rating_sell": clean(data.get("AnalystRatingSell"), int),
            "analyst_rating_strong_sell": clean(data.get("AnalystRatingStrongSell"), int),

            "trailing_pe": clean(data.get("TrailingPE"), float),
            "forward_pe": clean(data.get("ForwardPE"), float),
            "price_to_sales_ratio_ttm": clean(data.get("PriceToSalesRatioTTM"), float),
            "price_to_book_ratio": clean(data.get("PriceToBookRatio"), float),
            "ev_to_revenue": clean(data.get("EVToRevenue"), float),
            "ev_to_ebitda": clean(data.get("EVToEBITDA"), float),

            "beta": clean(data.get("Beta"), float),
            "week_52_high": clean(data.get("52WeekHigh"), float),
            "week_52_low": clean(data.get("52WeekLow"), float),
            "moving_avg_50d": clean(data.get("50DayMovingAverage"), float),
            "moving_avg_200d": clean(data.get("200DayMovingAverage"), float),

            "shares_outstanding": clean(data.get("SharesOutstanding"), int),
            "shares_float": clean(data.get("SharesFloat"), int),
            "percent_insiders": clean(data.get("PercentInsiders"), float),
            "percent_institutions": clean(data.get("PercentInstitutions"), float),

            "dividend_date": clean(data.get("DividendDate"), date),
            "ex_dividend_date": clean(data.get("ExDividendDate"), date)
        }

        cleaned_data.append(row)

    logger.info(f"Structured {len(cleaned_data)} overview rows")
    return cleaned_data


# Responsibility : Store the data into db
def store_data_to_db(cleaned_data, api_type):
    logger.info("Storing data to db....")
    # create_db()
    # create_table()
    load_data(cleaned_data, api_type)

# Responsibility : create table based on api_type
def create_table():
    engine = get_db_engine()
    Base.metadata.create_all(engine, tables=[MasterStockTable.__table__,
                                             MasterOverviewTable.__table__])  # this way we only create Ingestion tables right now
    logger.info("Ingestion Tables created if not present")


# Responsibilities : loads required sql file
def load_sql(filename: str):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # ingestion/
    sql_path = os.path.join(base_dir, "sql_scripts", filename)

    with open(sql_path, "r") as f:
        return f.read()


# Responsibility : load data to the required table for required api_type
def load_data(data, api_type):
    logger.info(f"Loading data for api_type={api_type}")
    if api_type == "timeseries":
        load_data_timeseries(data, "create_ingestion_timeseries_table.sql", f"{MY_DB}.{INGESTION_TIMESERIES_TABLE}")
    else:
        load_data_overview(data, "create_ingestion_overview_table.sql", f"{MY_DB}.{INGESTION_OVERVIEW_TABLE}")


# Responsibility : load data for timeseries master table
def load_data_timeseries(data, filename, target_table):
    engine = get_db_engine()

    columns = [
        "symbol",
        "timezone",
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

    normalized_data = []

    for row in data:  # this makes sure that if a column is missing from api response then my insert does not give error.
        # It simply adds that column and give it value None so that MySQL does not throw error
        if 'symbol' in row and row["symbol"] is not None and row["date"] is not None:
            fixed_row = {}
            for col in columns:
                fixed_row[col] = row[col] if col in row else None
            normalized_data.append(fixed_row)

    if not normalized_data:
        logger.warning("No valid timeseries rows to insert, skipping.")
        return  # ← exit cleanly instead of crashing

    raw_sql = load_sql(filename)
    final_sql = raw_sql.format(target_table=target_table)
    # debug level — full row dump is huge, only relevant when investigating issues
    logger.debug(f"Normalized timeseries data: {normalized_data}")
    logger.info(f"Inserting {len(normalized_data)} timeseries rows into {target_table}")

    try:
        with engine.connect() as conn:
            query = text(final_sql)
            conn.execute(query, normalized_data)
            conn.commit()
        logger.info(f"Timeseries data added to {target_table}")
    except Exception as e:
        # exc_info=True captures the full stack trace in the log — invaluable for debugging
        logger.error(f"Failed to insert timeseries data into {target_table}: {e}", exc_info=True)
        raise


# Responsibility : load data for overview master table
def load_data_overview(data, filename, target_table):
    engine = get_db_engine()
    columns = [
        "symbol",
        "asset_type", "name", "description", "cik", "exchange", "currency",
        "country", "sector", "industry", "address", "official_site", "fiscal_year_end", "latest_quarter",
        "market_capitalization", "ebitda", "pe_ratio", "peg_ratio", "book_value", "dividend_per_share",
        "dividend_yield", "eps", "revenue_per_share_ttm", "profit_margin", "operating_margin_ttm",
        "return_on_assets_ttm", "return_on_equity_ttm", "revenue_ttm", "gross_profit_ttm",
        "diluted_eps_ttm", "quarterly_earnings_growth_yoy", "quarterly_revenue_growth_yoy",
        "analyst_target_price", "analyst_rating_strong_buy", "analyst_rating_buy",
        "analyst_rating_hold", "analyst_rating_sell", "analyst_rating_strong_sell", "trailing_pe",
        "forward_pe", "price_to_sales_ratio_ttm", "price_to_book_ratio", "ev_to_revenue", "ev_to_ebitda",
        "beta", "week_52_high", "week_52_low", "moving_avg_50d", "moving_avg_200d", "shares_outstanding",
        "shares_float", "percent_insiders", "percent_institutions", "dividend_date", "ex_dividend_date"
    ]

    normalized_data = []
    for row in data:
        if 'symbol' in row and row["symbol"] is not None:
            fixed_row = {}
            for col in columns:
                fixed_row[col] = row[col] if col in row else None
            normalized_data.append(fixed_row)

    if not normalized_data:
        logger.warning("No valid overview rows to insert, skipping.")
        return  # ← exit cleanly instead of crashing

    raw_sql = load_sql(filename)
    final_sql = raw_sql.format(target_table=target_table)
    logger.debug(f"Normalized overview data: {normalized_data}")
    logger.info(f"Inserting {len(normalized_data)} overview rows into {target_table}")

    try:
        with engine.connect() as conn:
            query = text(final_sql)
            conn.execute(query, normalized_data)
            conn.commit()
        logger.info(f"Overview data added to {target_table}")
    except Exception as e:
        logger.error(f"Failed to insert overview data into {target_table}: {e}", exc_info=True)
        raise


# Responsibility : Api returns everything as String so it might return "None" for float type or any other unexpected result so in order to tackle that this function cleans the data if its weird
def clean(value, dtype):
    if value in (None, "", "None", "null", "N/A", "Null", "NULL", "NONE"):
        return None

    try:
        if dtype is str:
            return str(value)

        elif dtype is int:
            return int(value)

        elif dtype is float:
            return float(value)

        elif dtype is date:
            return datetime.strptime(value, "%Y-%m-%d").date()
        else:
            return value

    except Exception:
        return None