import streamlit as st


WATCHLIST = [
    "RELIANCE",
    "TCS",
    "INFY",
    "HDFCBANK",
    "ICICIBANK",
    "SBIN",
    "NIFTY",
    "BANKNIFTY",
]


def render():

    st.sidebar.title("⭐ Watchlist")

    symbol = st.sidebar.selectbox(

        "Select Symbol",

        WATCHLIST

    )

    st.sidebar.divider()

    st.sidebar.success("Market Connected")

    return symbol