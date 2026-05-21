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
import logging

# Module-level logger — name will be "transformation.transformation"
# Helps filter logs by module when debugging multi-layer pipelines
logger = logging.getLogger(__name__)


async def transform_data():
    logger.info("Starting transformation layer")
    create_table()
    run_all_transformations()
    logger.info("Transformation layer completed successfully")


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
    logger.info("Transformation tables created if not present")


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
    logger.info(f"Executing transformation: {filename} | {source_table} → {target_table}")
    raw_sql = load_sql(filename)

    # Inject table names into placeholders
    final_sql = raw_sql.format(source_table=source_table, target_table=target_table)
    # debug level — full SQL bodies are long; only useful when something's wrong
    logger.debug(f"Final SQL for {filename}: {final_sql}")

    engine = get_db_engine()
    try:
        with engine.begin() as conn:  # begin() auto-commits or rolls back on error
            conn.execute(text(final_sql))
        logger.info(f"{filename} executed successfully")
    except Exception as e:
        # exc_info=True attaches the full stack trace to the log entry
        # Critical for debugging SQL failures — tells you exactly which line broke
        logger.error(f"Failed to execute {filename}: {e}", exc_info=True)
        raise   # re-raise so pipeline halts properly and dashboard catches the failure