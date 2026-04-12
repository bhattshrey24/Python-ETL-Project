from sqlalchemy import Column, String, Float, Date, DateTime, BigInteger, Integer, Text
from sqlalchemy.sql import func

from config.db_constants import INGESTION_TIMESERIES_TABLE, INGESTION_OVERVIEW_TABLE
from db.my_db import Base

class MasterStockTable(Base):
    __tablename__ = INGESTION_TIMESERIES_TABLE

    symbol = Column(String(10),primary_key=True)
    ingestion_date = Column(DateTime, server_default=func.current_timestamp())

    timezone = Column(String(20))
    date = Column(Date,primary_key=True)

    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)

    volume = Column(BigInteger)

class MasterOverviewTable(Base):
    __tablename__ = INGESTION_OVERVIEW_TABLE

    symbol = Column(String(10),primary_key=True)
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