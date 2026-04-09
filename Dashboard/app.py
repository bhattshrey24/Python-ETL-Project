import sys
sys.path.insert(0, '/Users/shrey/PycharmProjects/PythonDEProject') # Tells streamlit where it is
# so that it can navigate project and find other imported files

import streamlit as st
import pandas as pd

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

df_ts = fetch_from_db("SELECT * FROM stocks_db.serving_timeseries_vw")
print(df_ts.head())
df_ma = fetch_from_db("SELECT * FROM stocks_db.serving_moving_averages_vw")
print(df_ma.head())
df_sp = fetch_from_db("SELECT * FROM stocks_db.serving_sector_performance_vw")
print(df_sp.head())
df_dsp = fetch_from_db("SELECT * FROM stocks_db.serving_daily_stock_performance_vw")
print(df_dsp.head())


st.set_page_config(
    page_title="Stocks Dashboard",  # the page title shown in the browser tab
    page_icon=":bar_chart:",  # the page favicon shown in the browser tab
    layout="wide",  # page layout : use the entire screen
)

st.title("My Stocks Dashboard")

# with st.expander('About The Dashboard'): # OPTIONAL
#     # st.header("About the Iris Dataset")
#     st.write("""The data is sourced from alpha vintage api. It contains past 20 years of daily stock data for 10
#     companies of various sectors along with their overview detail and some basic analysis""")

with st.sidebar:
    # add header
    st.header("Filters", divider=True)

    selected_type = st.selectbox("Select Type", ["Stocks", "Sector"])

    selected_company = None

    if selected_type == "Stocks":
        selected_company = st.selectbox("Select Company", ["AAPL", "MSFT","BMW"])

    print(selected_company)


if selected_type == "Stocks":

    print("Show Stocks graphs")

else :
    print("Show Sector graphs")


# st.header("Basic Statistics")
# st.dataframe(df.describe(), use_container_width=True) # use_container_width to True ensures the table stretches to fill the screen horizontally



