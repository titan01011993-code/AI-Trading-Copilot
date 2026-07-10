import streamlit as st

from dashboard.layout import configure_page, show_header
from dashboard.charts import CandlestickChart
from dashboard.sidebar import render
from indicators.rsi import RSIIndicator
from market.historical import HistoricalService
from indicators.ema import EMAIndicator
from indicators.macd import MACDIndicator
from indicators.volume import VolumeIndicator
from indicators.atr import ATRIndicator
from dashboard.ai_panel import render as render_ai
from dashboard.metrics import render as render_metrics
from dashboard.rsi_chart import RSIChart
from dashboard.macd_chart import MACDChart
from dashboard.volume_chart import VolumeChart

configure_page()

show_header()

history = HistoricalService()
symbol = render()

df = history.load(symbol)

df = EMAIndicator.calculate(df)
df = RSIIndicator.calculate(df)
df = MACDIndicator.calculate(df)
df = VolumeIndicator.calculate(df)
df = ATRIndicator.calculate(df)

render_metrics(df)

chart = CandlestickChart.build(df, symbol)

left, right = st.columns([4, 1], gap="large")

with left:
    st.plotly_chart(chart, use_container_width=True)
    
    rsi_chart = RSIChart.build(df)
    st.plotly_chart(rsi_chart, use_container_width=True)
    
    macd_chart = MACDChart.build(df)
    st.plotly_chart(macd_chart, use_container_width=True)
    
    volume_chart = VolumeChart.build(df)
    st.plotly_chart(volume_chart, use_container_width=True)

with right:
    render_ai(df, symbol=symbol)
