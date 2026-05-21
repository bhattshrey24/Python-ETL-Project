import sys
sys.path.insert(0, '/Users/shrey/PycharmProjects/PythonDEProject')

# NOTE : All the imports should start from here otherwise streamlit wont be able to find it


import logging
# Configure logging early — must happen before importing modules that log
logging.basicConfig( # logging here too because app.py is calling pipeline and not main.py where our logging is
    # defined so we have to define here again for dashboard
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

import asyncio
import threading
import queue
import time
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config.app_constants import COMPANIES
from config.db_constants import *
from db.my_db import get_db_engine
from pipeline import main as run_pipeline
from ingestion.ingestion import RateLimitError


# Use below command to run
# source /Users/shrey/PycharmProjects/PythonDEProject/.venv/bin/activate
# streamlit run /Users/shrey/PycharmProjects/PythonDEProject/dashboard/app.py

# NOTE : When a user moves a slider or clicks a button, Streamlit re-executes your entire script from top to bottom.



# REFRESH STATE MANAGEMENT
# Background threads can't write to st.session_state directly,
# so we use a thread-safe queue. Main thread reads from queue
# on each rerun and updates session_state from there.

if "refresh_status" not in st.session_state:
    st.session_state.refresh_status = "idle"
if "refresh_message" not in st.session_state:
    st.session_state.refresh_message = ""
if "refresh_start_time" not in st.session_state:
    st.session_state.refresh_start_time = None
if "result_queue" not in st.session_state:
    st.session_state.result_queue = queue.Queue()


def run_ingest_in_thread(result_queue):
    """
    Runs async ingest in background thread.
    Writes result to thread-safe queue (NOT session_state).
    """
    logging.info("⚙️ Pipeline starting in background thread")
    try:
        asyncio.run(run_pipeline())
        logging.info("✅ Pipeline completed in thread")
        result_queue.put(("success", "✅ Data refreshed successfully!"))
    except RateLimitError as e:
        result_queue.put(("rate_limit", f"⚠️ API limit hit: You have exceeded 25 requests per day limit. Kindly try again tomorrow!"))
    except Exception as e:
        result_queue.put(("error", f"❌ Refresh failed: {type(e).__name__}: {str(e)}"))


# CHECK FOR BACKGROUND THREAD RESULTS (runs on every rerun)
# Pull any completed result from queue BEFORE rendering charts,
# so cache can be cleared before dataframes are fetched.

if st.session_state.refresh_status == "running":
    try:
        # Non-blocking: only grab result if thread is done
        status, message = st.session_state.result_queue.get_nowait()
        st.session_state.refresh_status = status
        st.session_state.refresh_message = message

        if status == "success":
            st.cache_data.clear()  # ← clear BEFORE dataframes fetched below
    except queue.Empty:
        # Thread still running — check for timeout
        elapsed = time.time() - st.session_state.refresh_start_time
        if elapsed > 120:
            st.session_state.refresh_status = "timeout"
            st.session_state.refresh_message = (
                "⏱️ Refresh exceeded 1 minute. Showing previous data — "
                "background refresh may still complete."
            )


# FETCH DATA (cache cleared above if refresh succeeded)
# Wrapped in try/except so dashboard still loads even if tables don't exist yet (fresh install)
@st.cache_data # Without @st.cache_data, your CSV or SQL query re-runs on every widget interaction. This is the most common beginner mistake.
# You can set a TTL (time-to-live): @st.cache_data(ttl=300) — cache expires after 5 minutes, useful for live data.
def fetch_from_db(query): #  Cache is keyed on the function arguments. fetch_from_db(query1) and fetch_from_db(query2) are cached separately.
    try:
        conn = get_db_engine()
        return pd.read_sql(query, conn)     # DB hit only once per unique query
    except Exception as e:
        # If view doesn't exist yet (first run before any pipeline ran), return empty DataFrame
        # so dashboard still loads and refresh button is reachable
        logging.warning(f"Could not fetch from DB: {e}")
        return pd.DataFrame()


df_ts = fetch_from_db(f"SELECT * FROM {MY_DB}.{SERVING_TIMESERIES_VW}")
df_ma = fetch_from_db(f"SELECT * FROM {MY_DB}.{SERVING_STOCK_MOVING_AVERAGES_VW}")
df_sp = fetch_from_db(f"SELECT * FROM {MY_DB}.{SERVING_SECTOR_PERFORMANCE_VW}")
df_dsp = fetch_from_db(f"SELECT * FROM {MY_DB}.{SERVING_DAILY_STOCK_PERFORMANCE_VW}")
company_map = {c["name"]: c["symbol"] for c in COMPANIES}

# Detect global empty state — true when none of the views have any data
# Used later to show a friendly "no data" message instead of crashing on empty charts
all_data_empty = df_ts.empty and df_ma.empty and df_sp.empty and df_dsp.empty


st.set_page_config(
    page_title="Stocks Dashboard",  # the page title shown in the browser tab
    page_icon=":bar_chart:", # the page favicon shown in the browser tab
    layout="wide", # page layout : use the entire screen
)
st.title("My Stocks Analysis Dashboard")

with st.sidebar:
    st.header("Filters", divider=True)
    selected_type = st.selectbox("Select Type", ["Stocks", "Sector"])
    selected_company = None
    if selected_type == "Stocks":
        selected_company = st.selectbox(
            "Select Company", [c['name'] for c in COMPANIES]
        )

    st.divider()

    is_running = st.session_state.refresh_status == "running"

    if st.button("🔄 Refresh Data", disabled=is_running, use_container_width=True):
        logging.info("🔘 Refresh button clicked — starting pipeline thread")
        st.session_state.refresh_status = "running"
        st.session_state.refresh_message = ""
        st.session_state.refresh_start_time = time.time()

        # Pass the queue explicitly (don't access session_state from thread)
        thread = threading.Thread(
            target=run_ingest_in_thread,
            args=(st.session_state.result_queue,),
            daemon=True
        )
        thread.start()
        st.rerun()

    # Status display
    status = st.session_state.refresh_status

    if status == "running":
        elapsed = int(time.time() - st.session_state.refresh_start_time)
        st.info(f"⏳ Refreshing... ({elapsed}s elapsed)")
        # Auto-rerun every 2s to poll thread and update elapsed counter
        time.sleep(2)
        st.rerun()

    elif status == "success":
        st.success(st.session_state.refresh_message)

    elif status == "rate_limit":
        st.warning(st.session_state.refresh_message)

    elif status == "timeout":
        st.warning(st.session_state.refresh_message)

    elif status == "error":
        st.error(st.session_state.refresh_message)


def show_stocks_graph():
        # Guard against empty/missing data for the selected symbol
        # Without this guard, plotly tries to render empty data and pandas .iloc[0] crashes
        if df_ts_curr_symbol.empty:
            st.info("📭 No stock data available for this company. Click 'Refresh Data' in the sidebar to fetch.")
            return

        fig_bar = px.line(df_ts_curr_symbol, x="date", y="close",markers=True, title="Stock Price History")
        st.plotly_chart(fig_bar,use_container_width=True, key="chart_col1")

        # selected_ma = st.selectbox("Select Company", ["7 Days", "10 Days", "20 Days","50 Days","100 Days","200 Days"])
        selected_ma = st.selectbox("Select MA Type",options=["All", "MA 7 Days", "MA 10 Days", "MA 20 Days", "MA 50 Days", "MA 100 Days", "MA 200 Days"],key="ma_selector")
        ma_config = {
            "MA 7 Days": {"col": "ma_7", "color": "orange"},
            "MA 10 Days": {"col": "ma_10", "color": "green"},
            "MA 20 Days": {"col": "ma_20", "color": "yellow"},
            "MA 50 Days": {"col": "ma_50", "color": "blue"},
            "MA 100 Days": {"col": "ma_100", "color": "red"},
            "MA 200 Days": {"col": "ma_200", "color": "purple"}
        }
        to_plot = ma_config.keys() if selected_ma == "All" else [selected_ma]

        fig = go.Figure()

        # Only render MA chart if MA data is available
        if not df_ma_curr_symbol.empty:
            for name in to_plot:
                cfg = ma_config[name]
                fig.add_trace(go.Scatter(
                    x=df_ma_curr_symbol["date"],
                    y=df_ma_curr_symbol[cfg["col"]],
                    mode="lines",
                    name=name,
                    line=dict(color=cfg["color"], width=1.5)
                ))

            fig.update_layout(title="Moving Averages")
            st.plotly_chart(fig, use_container_width=True, key="ma_chart")
        else:
            st.info("📭 No moving average data available for this company.")

        # Daily performance metrics — guard against empty DSP data
        if not df_dsp_curr_symbol.empty:
            latest_date = df_dsp_curr_symbol['date'].max()
            df_latest = df_dsp_curr_symbol[df_dsp_curr_symbol['date'] == latest_date][['gap_open_pct', 'volume_change', 'percentage_change','close', 'volume','prev_volume']]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    label="Latest Close Price",
                    value= f"{df_latest["close"].iloc[0].round(2)}",
                    delta= f"{df_latest["percentage_change"].iloc[0].round(2)} %"  # green if positive, red if negative automatically
                )
            with col2:
                st.metric(
                    label="Latest Volume",
                    value=f"{df_latest["volume"].iloc[0].round(2)}",
                    delta=f"{((df_latest["volume_change"].iloc[0]/df_latest["prev_volume"].iloc[0])*100).round(2)} %"  # green if positive, red if negative automatically
                )
            with col3:
                st.metric(
                    label="Latest Opening Gap",
                    value=f"{df_latest["gap_open_pct"].iloc[0].round(2)} %"
                )
        else:
            st.info("📭 No daily performance data available for this company.")

def show_sector_graph():
    # Guard against empty sector data — without this, plotly bar charts render empty placeholders
    if df_sp.empty:
        st.info("📭 No sector data available. Click 'Refresh Data' in the sidebar to fetch.")
        return

    col1, col2 = st.columns(2,gap='large')
    with col1:
        fig = px.bar(
            df_sp,
            x="sector",
            y="total_market_cap",  # showing volume as bars
            color="sector",
            title="Total Market Cap",
        )
        st.plotly_chart(fig, use_container_width=True, key="market_cap_bar")
    with col2:
        fig2 = px.bar(
            df_sp,
            x="sector",
            y="avg_pe_ratio",  # showing volume as bars
            color="sector",
            title="Average PE Ratio",
        )
        st.plotly_chart(fig2, use_container_width=True, key="avg_pe_bar")
    col3, col4 = st.columns(2,gap='large')
    with col3:
        fig3 = px.bar(
            df_sp,
            x="sector",
            y="avg_beta",  # showing volume as bars
            color="sector",
            title="Average BETA",
        )
        st.plotly_chart(fig3, use_container_width=True, key="avg_beta_bar")
    with col4:
        fig4 = px.bar(
            df_sp,
            x="sector",
            y="company_count",  # showing volume as bars
            color="sector",
            title="Company Count",
        )
        st.plotly_chart(fig4, use_container_width=True, key="company_count_bar")
    sector_config = {
        "Average EPS" : "avg_eps",
        "Average Profit Margin" : "avg_profit_margin",
        "Average Market Cap" : "avg_market_cap_by_sector",
    }
    selected_compare_type = st.selectbox("Select Type", ["Average EPS", "Average Profit Margin", "Average Market Cap"])
    fig4 = px.bar(
        df_sp,
        x="sector",
        y=f"{sector_config[selected_compare_type]}",  # showing volume as bars
        color="sector",
        title="Compare Sectors",
    )
    st.plotly_chart(fig4, use_container_width=True, key="compare_sector_bar")


# Show top-level banner when entire DB is empty (first-run state)
# Sidebar still has the refresh button — user can trigger pipeline from there
if all_data_empty:
    st.warning("📭 **No data available yet.** Click the **🔄 Refresh Data** button in the sidebar to fetch data from the API.")
    st.warning("⚠️ Note : It might take 1-2 minutes to refresh the data since we are using free tier")

if selected_type == "Stocks":

    selected_symbol = company_map.get(selected_company)

    # Slice DataFrames per symbol — but only if source DataFrames are non-empty
    # Empty source → empty slice (which is what we want; the show_stocks_graph guards handle it)
    df_ts_curr_symbol = df_ts[df_ts['symbol'] == selected_symbol] if not df_ts.empty else df_ts
    df_ma_curr_symbol = df_ma[df_ma['symbol']  == selected_symbol] if not df_ma.empty else df_ma
    df_dsp_curr_symbol = df_dsp[df_dsp['symbol']  == selected_symbol] if not df_dsp.empty else df_dsp

    show_stocks_graph()

else :
    show_sector_graph()