from config.db_constants import (
    TRANSFORMATION_CLEANED_TIMESERIES_TABLE,
    TRANSFORMATION_BAD_TIMESERIES_TABLE,
    TRANSFORMATION_CLEANED_OVERVIEW_TABLE,
    TRANSFORMATION_BAD_OVERVIEW_TABLE,
    MY_DB,
    INGESTION_OVERVIEW_TABLE,
    INGESTION_TIMESERIES_TABLE,
    TRANSFORMATION_DAILY_STOCK_PERFORMANCE_TABLE,
    TRANSFORMATION_SECTOR_PERFORMANCE_TABLE,
    TRANSFORMATION_STOCK_MOVING_AVERAGES_TABLE,
)
from sqlalchemy import text
from db.my_db import get_db_engine, Base
from transformation.models import CleanedTimeseriesTable, BadTimeseriesTable, CleanedOverviewTable, BadOverviewTable, \
    DailyStockPerformance, StockMovingAverages, SectorPerformance
import os


async def transform_data():
    create_table()
    run_all_transformations()
    print("Transforming data....")


def run_all_transformations():
    execute_transformation(
        filename="create_clean_overview_table.sql",
        target_table=f"{MY_DB}.{TRANSFORMATION_CLEANED_OVERVIEW_TABLE}",
        source_table=f"{MY_DB}.{INGESTION_OVERVIEW_TABLE}",
    )
    execute_transformation(
        filename="create_clean_timeseries_table.sql",
        target_table=f"{MY_DB}.{TRANSFORMATION_CLEANED_TIMESERIES_TABLE}",
        source_table=f"{MY_DB}.{INGESTION_TIMESERIES_TABLE}",
    )
    execute_transformation(
        filename="create_bad_overview_table.sql",
        target_table=f"{MY_DB}.{TRANSFORMATION_BAD_OVERVIEW_TABLE}",
        source_table=f"{MY_DB}.{INGESTION_OVERVIEW_TABLE}",
    )
    execute_transformation(
        filename="create_bad_timeseries_table.sql",
        target_table=f"{MY_DB}.{TRANSFORMATION_BAD_TIMESERIES_TABLE}",
        source_table=f"{MY_DB}.{INGESTION_TIMESERIES_TABLE}",
    )
    execute_transformation(
        filename="create_daily_stock_performance_table.sql",
        target_table=f"{MY_DB}.{TRANSFORMATION_DAILY_STOCK_PERFORMANCE_TABLE}",
        source_table=f"{MY_DB}.{TRANSFORMATION_CLEANED_TIMESERIES_TABLE}",
    )
    execute_transformation(
        filename="create_sector_performance_table.sql",
        target_table=f"{MY_DB}.{TRANSFORMATION_SECTOR_PERFORMANCE_TABLE}",
        source_table=f"{MY_DB}.{TRANSFORMATION_CLEANED_OVERVIEW_TABLE}",
    )
    execute_transformation(
        filename="create_stock_moving_averages_table.sql",
        target_table=f"{MY_DB}.{TRANSFORMATION_STOCK_MOVING_AVERAGES_TABLE}",
        source_table=f"{MY_DB}.{TRANSFORMATION_CLEANED_TIMESERIES_TABLE}",
    )


def create_table():
    engine = get_db_engine()
    Base.metadata.create_all(
        engine,
        tables=[
            CleanedTimeseriesTable.__table__,
            BadTimeseriesTable.__table__,
            CleanedOverviewTable.__table__,
            BadOverviewTable.__table__,
            DailyStockPerformance.__table__,
            StockMovingAverages.__table__,
            SectorPerformance.__table__,
        ],
    )
    print("Transformation tables created if not present")


def load_sql(filename: str):
    """
    Reads a .sql file from the sql_scripts directory.
    Keeps file resolution relative to this file's location.
    """

    base_dir = os.path.dirname(os.path.abspath(__file__))  # transformation/
    sql_path = os.path.join(base_dir, "sql_scripts", filename)

    with open(sql_path, "r") as f:
        return f.read()


def execute_transformation(filename: str, source_table: str, target_table: str):
    """
    Loads a SQL file, injects table names, and executes it.
    Args:
        filename:     SQL file name e.g. 'daily_performance.sql'
        source_table: Fully qualified source e.g. 'stocks_db.transformation_cleaned_timeseries_table'
        target_table: Fully qualified target e.g. 'stocks_db.transformation_daily_performance_table'
    """
    raw_sql = load_sql(filename)

    # Inject table names into placeholders
    final_sql = raw_sql.format(source_table=source_table, target_table=target_table)
    engine = get_db_engine()
    with engine.begin() as conn:  # begin() auto-commits or rolls back on error
        conn.execute(text(final_sql))
        print(f"{filename} executed successfully")
