import requests
import asyncio

from sqlalchemy import text

from config.app_constants import *
from datetime import datetime, timezone, date
from config.db_constants import INGESTION_TIMESERIES_TABLE, \
    INGESTION_OVERVIEW_TABLE  # I guess this triggers registering of these ORM classes to Base
from db.my_db import *
from dotenv import load_dotenv
from ingestion.models import *

load_dotenv()


# Responsibility : Ingest data from different URLs
async def ingest_data():
    # timeseries_response = await ingest_from_api("TIME_SERIES_DAILY")  # ingest stock details for 10 symbols
    overview_response = await ingest_from_api("OVERVIEW")  # ingest overview details for 10 symbols
    print("Got timeseries data for all symbols")
    print(f"Got overview data for all symbols {overview_response}")
    # timeseries_changed_structure = change_structure(timeseries_response, "timeseries")
    overview_changed_structure = change_structure(overview_response, "overview")
    # store_data_to_db(timeseries_changed_structure, "timeseries")
    store_data_to_db(overview_changed_structure, "overview")


# Responsibility : To call api with required parameters for all symbols and aggregate the result
async def ingest_from_api(function):
    complete_result = []  # list of json response i.e. dictionary
    for company in COMPANIES:
        result = await ingest_data_for_symbol(symbol=company['symbol'], function=function)
        complete_result.append(result)
    return complete_result


# Responsibility : To call api and get result for single symbol
async def ingest_data_for_symbol(symbol, function):
    await asyncio.sleep(1)  # due to API limitation in free package we have to add 1 second delay
    api_key = os.getenv("API_KEY")
    url = f"{BASE_URL}query?function={function}&symbol={symbol}&apikey={api_key}"
    return requests.get(url).json()  # todo change this to aiohttp since requests is actually blocking


# Responsibility : To change the json response into the required table structure
def change_structure(response, api_type):
    if api_type == "timeseries":
        data = change_structure_for_timeseries(response)
    else:
        data = change_structure_for_overview(response)
    return data


# Responsibility : To change structure for overview response into the required table structure
def change_structure_for_timeseries(response):
    print(response)
    cleaned_data = []  # list of dictionaries where each row is a dictionary
    for data in response:
        meta = data.get("Meta Data",
                        {})  # if key "Meta Data" is not present then this will return empty dictionary instead of None
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

    return cleaned_data


# Responsibility : To change structure for overview response into the required table structure
def change_structure_for_overview(response):
    print(response)
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

    return cleaned_data


# Responsibility : Store the data into db
def store_data_to_db(cleaned_data, api_type):
    print("Storing data to db....")
    create_db()
    create_table()
    load_data(cleaned_data, api_type)


# Responsibility : create database if not exist
def create_db():
    engine = get_app_engine()
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db}"))
        conn.commit()
        print("Database created")


# Responsibility : create table based on api_type
def create_table():
    engine = get_db_engine()
    Base.metadata.create_all(engine, tables=[MasterStockTable.__table__,
                                             MasterOverviewTable.__table__])  # this way we only create Ingestion tables right now
    print("Ingestion Tables created if not present")


# Responsibilities : loads required sql file
def load_sql(filename: str):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # ingestion/
    sql_path = os.path.join(base_dir, "sql_scripts", filename)

    with open(sql_path, "r") as f:
        return f.read()


# Responsibility : load data to the required table for required api_type
def load_data(data, api_type):
    print("Loading data....")
    if api_type == "timeseries":
        load_data_timeseries(data, "create_ingestion_timeseries_table.sql", f"{MY_DB}.{INGESTION_TIMESERIES_TABLE}")
    else:
        load_data_overview(data, "create_ingestion_overview_table.sql", f"{MY_DB}.{INGESTION_OVERVIEW_TABLE}")


# Responsibility : load data for timeseries master table
def load_data_timeseries(data, filename, target_table):
    engine = get_db_engine()

    columns = [
        "symbol",
        # "ingestion_date",
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

    raw_sql = load_sql(filename)
    final_sql = raw_sql.format(target_table=target_table)

    with engine.connect() as conn:
        query = text(final_sql)
        conn.execute(query, normalized_data)
        conn.commit()

    print("Data added to table")


# Responsibility : load data for overview master table
def load_data_overview(data, filename, target_table):
    engine = get_db_engine()
    columns = [
        "symbol",
        # "ingestion_date",
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

    raw_sql = load_sql(filename)
    final_sql = raw_sql.format(target_table=target_table)

    with engine.connect() as conn:
        query = text(final_sql)
        conn.execute(query, normalized_data)
        conn.commit()

    print("Overview data added to table")


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
