import sys
sys.path.insert(0, '/Users/shrey/PycharmProjects/PythonDEProject') # Tells streamlit where it is
# so that it can navigate project and find other imported files

# NOTE : All the imports should start from here otherwise streamlit wont be able to find it
from config.app_constants import COMPANIES
from config.db_constants import *
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from db.my_db import get_db_engine

# Use below command to run
# source /Users/shrey/PycharmProjects/PythonDEProject/.venv/bin/activate
# streamlit run /Users/shrey/PycharmProjects/PythonDEProject/dashboard/app.py

# NOTE : When a user moves a slider or clicks a button, Streamlit re-executes your entire script from top to bottom.

@st.cache_data # Without @st.cache_data, your CSV or SQL query re-runs on every widget interaction. This is the most common beginner mistake.
# You can set a TTL (time-to-live): @st.cache_data(ttl=300) — cache expires after 5 minutes, useful for live data.
def fetch_from_db(query): # Cache is keyed on the function arguments. fetch_from_db(query1) and fetch_from_db(query2) are cached separately.
    conn = get_db_engine()
    return pd.read_sql(query, conn)      # DB hit only once per unique query

df_ts = fetch_from_db(f"SELECT * FROM {MY_DB}.{SERVING_TIMESERIES_VW}")
print(df_ts.head())
df_ma = fetch_from_db(f"SELECT * FROM {MY_DB}.{SERVING_STOCK_MOVING_AVERAGES_VW}")
print(df_ma.head())
df_sp = fetch_from_db(f"SELECT * FROM {MY_DB}.{SERVING_SECTOR_PERFORMANCE_VW}")
print(df_sp.head())
df_dsp = fetch_from_db(f"SELECT * FROM {MY_DB}.{SERVING_DAILY_STOCK_PERFORMANCE_VW}")
print(df_dsp.head())
company_map = {c["name"]: c["symbol"] for c in COMPANIES} # For ease of searching


st.set_page_config(
    page_title="Stocks Dashboard",  # the page title shown in the browser tab
    page_icon=":bar_chart:",  # the page favicon shown in the browser tab
    layout="wide",  # page layout : use the entire screen
)

st.title("My Stocks Analysis Dashboard")

# with st.expander('About The Dashboard'): # OPTIONAL
#     # st.header("About the Iris Dataset")
#     st.write("""The data is sourced from alpha vintage api. It contains past 20 years of daily stock data for 10
#     companies of various sectors along with their overview detail and some basic analysis""")

with st.sidebar:
    st.header("Filters", divider=True)
    selected_type = st.selectbox("Select Type", ["Stocks", "Sector"])
    selected_company = None
    if selected_type == "Stocks":
        selected_company = st.selectbox("Select Company", [company['name'] for  company in COMPANIES])
    print(selected_type)
    print(selected_company)


def show_stocks_graph():

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

def show_sector_graph():
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

if selected_type == "Stocks":

    selected_symbol = company_map.get(selected_company)

    df_ts_curr_symbol = df_ts[df_ts['symbol'] == selected_symbol]
    df_ma_curr_symbol = df_ma[df_ma['symbol']  == selected_symbol]
    df_dsp_curr_symbol = df_dsp[df_dsp['symbol']  == selected_symbol]

    show_stocks_graph()
    print(f"Show Stocks graphs {selected_symbol}")

else :
    show_sector_graph()
    print("Show Sector graphs")




