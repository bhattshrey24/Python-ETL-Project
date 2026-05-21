import os
import logging

from sqlalchemy import text

from config.db_constants import MY_DB, SERVING_TIMESERIES_VW, TRANSFORMATION_CLEANED_TIMESERIES_TABLE, \
    SERVING_OVERVIEW_VW, TRANSFORMATION_CLEANED_OVERVIEW_TABLE, SERVING_DAILY_STOCK_PERFORMANCE_VW, \
    TRANSFORMATION_DAILY_STOCK_PERFORMANCE_TABLE, SERVING_SECTOR_PERFORMANCE_VW, \
    TRANSFORMATION_SECTOR_PERFORMANCE_TABLE, SERVING_STOCK_MOVING_AVERAGES_VW, \
    TRANSFORMATION_STOCK_MOVING_AVERAGES_TABLE
from db.my_db import get_db_engine

# Module-level logger — name will be "serving.serving"
# Lets you filter logs per pipeline layer (ingestion / transformation / serving) when debugging
logger = logging.getLogger(__name__)


async def serve_data():
    logger.info("Starting serving layer")
    create_views()
    logger.info("Serving layer completed successfully")


def create_views():
    execute_transformation(
        filename="create_timeseries_vw.sql",
        view_name=f"{MY_DB}.{SERVING_TIMESERIES_VW}",
        source_table=f"{MY_DB}.{TRANSFORMATION_CLEANED_TIMESERIES_TABLE}",
    )
    execute_transformation(
        filename="create_overview_vw.sql",
        view_name=f"{MY_DB}.{SERVING_OVERVIEW_VW}",
        source_table=f"{MY_DB}.{TRANSFORMATION_CLEANED_OVERVIEW_TABLE}",
    )
    execute_transformation(
        filename="create_daily_stock_performance_vw.sql",
        view_name=f"{MY_DB}.{SERVING_DAILY_STOCK_PERFORMANCE_VW}",
        source_table=f"{MY_DB}.{TRANSFORMATION_DAILY_STOCK_PERFORMANCE_TABLE}",
    )
    execute_transformation(
        filename="create_sector_performance_vw.sql",
        view_name=f"{MY_DB}.{SERVING_SECTOR_PERFORMANCE_VW}",
        source_table=f"{MY_DB}.{TRANSFORMATION_SECTOR_PERFORMANCE_TABLE}",
    )
    execute_transformation(
        filename="create_stock_moving_averages_vw.sql",
        view_name=f"{MY_DB}.{SERVING_STOCK_MOVING_AVERAGES_VW}",
        source_table=f"{MY_DB}.{TRANSFORMATION_STOCK_MOVING_AVERAGES_TABLE}",
    )
    logger.info("All views created")


def load_sql(filename: str):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # serving/
    sql_path = os.path.join(base_dir, "sql_scripts", filename)

    with open(sql_path, "r") as f:
        return f.read()


def execute_transformation(filename: str, source_table: str, view_name: str):
    logger.info(f"Creating view: {filename} | source={source_table} → view={view_name}")
    raw_sql = load_sql(filename)

    # Inject table names into placeholders
    final_sql = raw_sql.format(source_table=source_table, view_name=view_name)
    # debug level — full DDL bodies are long; only useful when something's wrong
    logger.debug(f"Final SQL for {filename}: {final_sql}")

    engine = get_db_engine()
    try:
        with engine.begin() as conn:  # begin() auto-commits or rolls back on error
            conn.execute(text(final_sql))
        logger.info(f"{filename} executed successfully")
    except Exception as e:
        # exc_info=True captures the full stack trace — critical for spotting which view definition broke
        logger.error(f"Failed to execute {filename}: {e}", exc_info=True)
        raise   # re-raise so pipeline halts and Streamlit can show the failure