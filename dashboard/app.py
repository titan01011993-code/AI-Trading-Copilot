import streamlit as st

from dashboard.layout import configure_page, show_header
from dashboard.charts import CandlestickChart

from market.historical import HistoricalService

configure_page()

show_header()


history = HistoricalService()

symbol = st.text_input(

    "Stock Symbol",

    value="RELIANCE"

).upper()


df = history.load(symbol)


chart = CandlestickChart.build(

    df,

    symbol

)

st.plotly_chart(

    chart,

    use_container_width=True

)


col1, col2, col3 = st.columns(3)

col1.metric(

    "Trend",

    "Bullish"

)

col2.metric(

    "AI Signal",

    "BUY"

)

col3.metric(

    "Confidence",

    "91%"

)