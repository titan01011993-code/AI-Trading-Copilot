import streamlit as st

st.set_page_config(
    page_title="AI Trading Copilot",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AI Trading Copilot")

st.success("Broker Status : Connected")

symbol = st.text_input(
    "Search Symbol",
    value="RELIANCE"
)

col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Chart")
    st.info("Candlestick chart will appear here.")

with col2:
    st.subheader("AI Recommendation")

    st.metric("Signal", "BUY")

    st.metric("Confidence", "91 %")

    st.metric("Trend", "Bullish")

st.divider()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("EMA20", "Bullish")

with c2:
    st.metric("RSI", "63")

with c3:
    st.metric("MACD", "Bullish")