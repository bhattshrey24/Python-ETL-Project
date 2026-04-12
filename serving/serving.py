import os

from sqlalchemy import text

from config.db_constants import MY_DB, SERVING_TIMESERIES_VW, TRANSFORMATION_CLEANED_TIMESERIES_TABLE, \
    SERVING_OVERVIEW_VW, TRANSFORMATION_CLEANED_OVERVIEW_TABLE, SERVING_DAILY_STOCK_PERFORMANCE_VW, \
    TRANSFORMATION_DAILY_STOCK_PERFORMANCE_TABLE, SERVING_SECTOR_PERFORMANCE_VW, \
    TRANSFORMATION_SECTOR_PERFORMANCE_TABLE, SERVING_STOCK_MOVING_AVERAGES_VW, \
    TRANSFORMATION_STOCK_MOVING_AVERAGES_TABLE
from db.my_db import get_db_engine


async def serve_data():
    create_views()
    print("exposing data ...")


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
    print("views created")


def load_sql(filename: str):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # serving/
    sql_path = os.path.join(base_dir, "sql_scripts", filename)

    with open(sql_path, "r") as f:
        return f.read()


def execute_transformation(filename: str, source_table: str, view_name: str):
    raw_sql = load_sql(filename)

    # Inject table names into placeholders
    final_sql = raw_sql.format(source_table=source_table, view_name=view_name)
    engine = get_db_engine()
    with engine.begin() as conn:  # begin() auto-commits or rolls back on error
        conn.execute(text(final_sql))
        print(f"{filename} executed successfully")
