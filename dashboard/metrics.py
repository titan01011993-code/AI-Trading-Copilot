import streamlit as st


def render(df):

    last = df.iloc[-1]

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Close",
        f"₹ {last['close']:.2f}"
    )

    c2.metric(
        "Open",
        f"₹ {last['open']:.2f}"
    )

    c3.metric(
        "High",
        f"₹ {last['high']:.2f}"
    )

    c4.metric(
        "Low",
        f"₹ {last['low']:.2f}"
    )

    c5.metric(
        "Volume",
        f"{int(last['volume']):,}"
    )