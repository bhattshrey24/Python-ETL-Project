from sqlalchemy import Column, String, Float, Date, DateTime, BigInteger, Integer, Text, Boolean
from sqlalchemy.sql import func

from config.db_constants import *
from db.my_db import Base

class CleanedTimeseriesTable(Base):
    __tablename__ = TRANSFORMATION_CLEANED_TIMESERIES_TABLE

    date = Column(Date,  primary_key=True)
    symbol = Column(String(10),  primary_key=True) # because on a single day for each company there will be just one OHLC

    ingestion_date = Column(DateTime, server_default=func.current_timestamp())

    timezone = Column(String(20))

    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)

    volume = Column(BigInteger)

class BadTimeseriesTable(Base):

    __tablename__ = TRANSFORMATION_BAD_TIMESERIES_TABLE
    id = Column(BigInteger, primary_key=True, autoincrement=True) # creating surrogate key because API can give any row as null so we cannot make any row as PK right now

    date = Column(Date)
    symbol = Column(String(10)) # because on a single day for each company there will be just one OHLC

    ingestion_date = Column(DateTime, server_default=func.current_timestamp())

    timezone = Column(String(20))

    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)

    volume = Column(BigInteger)
    reason = Column(Text)

class CleanedOverviewTable(Base):
    __tablename__ = TRANSFORMATION_CLEANED_OVERVIEW_TABLE

    symbol = Column(String(10), primary_key=True)

    ingestion_date = Column(DateTime, server_default=func.current_timestamp())

    asset_type = Column(String(50))
    name = Column(String(255))
    description = Column(Text)

    cik = Column(String(20))
    exchange = Column(String(20))
    currency = Column(String(10))
    country = Column(String(50))

    sector = Column(String(100))
    industry = Column(String(150))

    address = Column(Text)
    official_site = Column(String(255))

    fiscal_year_end = Column(String(20))
    latest_quarter = Column(Date)

    market_capitalization = Column(BigInteger)
    ebitda = Column(BigInteger)

    pe_ratio = Column(Float)
    peg_ratio = Column(Float)
    book_value = Column(Float)

    dividend_per_share = Column(Float)
    dividend_yield = Column(Float)

    eps = Column(Float)
    revenue_per_share_ttm = Column(Float)

    profit_margin = Column(Float)
    operating_margin_ttm = Column(Float)

    return_on_assets_ttm = Column(Float)
    return_on_equity_ttm = Column(Float)

    revenue_ttm = Column(BigInteger)
    gross_profit_ttm = Column(BigInteger)

    diluted_eps_ttm = Column(Float)

    quarterly_earnings_growth_yoy = Column(Float)
    quarterly_revenue_growth_yoy = Column(Float)

    analyst_target_price = Column(Float)

    analyst_rating_strong_buy = Column(Integer)
    analyst_rating_buy = Column(Integer)
    analyst_rating_hold = Column(Integer)
    analyst_rating_sell = Column(Integer)
    analyst_rating_strong_sell = Column(Integer)

    trailing_pe = Column(Float)
    forward_pe = Column(Float)

    price_to_sales_ratio_ttm = Column(Float)
    price_to_book_ratio = Column(Float)

    ev_to_revenue = Column(Float)
    ev_to_ebitda = Column(Float)

    beta = Column(Float)

    week_52_high = Column(Float)
    week_52_low = Column(Float)

    moving_avg_50d = Column(Float)
    moving_avg_200d = Column(Float)

    shares_outstanding = Column(BigInteger)
    shares_float = Column(BigInteger)

    percent_insiders = Column(Float)
    percent_institutions = Column(Float)

    dividend_date = Column(Date)
    ex_dividend_date = Column(Date)

class BadOverviewTable(Base):
    __tablename__ = TRANSFORMATION_BAD_OVERVIEW_TABLE

    id = Column(BigInteger, primary_key=True, autoincrement=True) # creating surrogate key because API can give any row as null so we cannot make any row as PK right now

    symbol = Column(String(10))
    ingestion_date = Column(DateTime)

    asset_type = Column(String(50))
    name = Column(String(255))
    description = Column(Text)

    cik = Column(String(20))
    exchange = Column(String(20))
    currency = Column(String(10))
    country = Column(String(50))

    sector = Column(String(100))
    industry = Column(String(150))

    address = Column(Text)
    official_site = Column(String(255))

    fiscal_year_end = Column(String(20))
    latest_quarter = Column(Date)

    market_capitalization = Column(BigInteger)
    ebitda = Column(BigInteger)

    pe_ratio = Column(Float)
    peg_ratio = Column(Float)
    book_value = Column(Float)

    dividend_per_share = Column(Float)
    dividend_yield = Column(Float)

    eps = Column(Float)
    revenue_per_share_ttm = Column(Float)

    profit_margin = Column(Float)
    operating_margin_ttm = Column(Float)

    return_on_assets_ttm = Column(Float)
    return_on_equity_ttm = Column(Float)

    revenue_ttm = Column(BigInteger)
    gross_profit_ttm = Column(BigInteger)

    diluted_eps_ttm = Column(Float)

    quarterly_earnings_growth_yoy = Column(Float)
    quarterly_revenue_growth_yoy = Column(Float)

    analyst_target_price = Column(Float)

    analyst_rating_strong_buy = Column(Integer)
    analyst_rating_buy = Column(Integer)
    analyst_rating_hold = Column(Integer)
    analyst_rating_sell = Column(Integer)
    analyst_rating_strong_sell = Column(Integer)

    trailing_pe = Column(Float)
    forward_pe = Column(Float)

    price_to_sales_ratio_ttm = Column(Float)
    price_to_book_ratio = Column(Float)

    ev_to_revenue = Column(Float)
    ev_to_ebitda = Column(Float)

    beta = Column(Float)

    week_52_high = Column(Float)
    week_52_low = Column(Float)

    moving_avg_50d = Column(Float)
    moving_avg_200d = Column(Float)

    shares_outstanding = Column(BigInteger)
    shares_float = Column(BigInteger)

    percent_insiders = Column(Float)
    percent_institutions = Column(Float)

    dividend_date = Column(Date)
    ex_dividend_date = Column(Date)
    reason = Column(Text)

class DailyStockPerformance(Base):

    __tablename__ = TRANSFORMATION_DAILY_STOCK_PERFORMANCE_TABLE

    symbol = Column(String(10),primary_key=True)
    date = Column(Date, primary_key=True)
    ingestion_date = Column(DateTime, server_default=func.current_timestamp())
    timezone = Column(String(20))

    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)

    prev_open = Column(Float) # So that we don't have to do lag again and again at Reporting side
    prev_high = Column(Float)
    prev_low = Column(Float)
    prev_close = Column(Float)
    prev_volume = Column(BigInteger)

    price_change = Column(Float)
    percentage_change = Column(Float)
    volume_change = Column(Float)
    gap_open_pct = Column(Float)
    is_positive_day = Column(Integer)

class StockMovingAverages(Base):
        __tablename__ = TRANSFORMATION_STOCK_MOVING_AVERAGES_TABLE
        symbol = Column(String(10),primary_key=True)
        date = Column(Date, primary_key=True)
        ingestion_date = Column(DateTime, server_default=func.current_timestamp())
        timezone = Column(String(20))
        close = Column(Float)
        ma_7 = Column(Float)
        ma_10 = Column(Float)
        ma_20 = Column(Float)
        ma_50 = Column(Float)
        ma_100 = Column(Float)
        ma_200 = Column(Float)
        golden_cross = Column(Integer)
        death_cross = Column(Integer)

class SectorPerformance(Base):
    __tablename__ = TRANSFORMATION_SECTOR_PERFORMANCE_TABLE
    sector = Column(String(100),primary_key=True)
    ingestion_date = Column(DateTime, server_default=func.current_timestamp())
    avg_market_cap_by_sector = Column(Float)
    total_market_cap = Column(Float)
    max_market_cap = Column(Float)
    min_market_cap = Column(Float)
    avg_pe_ratio = Column(Float)
    avg_eps = Column(Float)
    avg_profit_margin = Column(Float)
    avg_beta = Column(Float)
    company_count = Column(Float)
    top_company_by_market_cap = Column(String(10))