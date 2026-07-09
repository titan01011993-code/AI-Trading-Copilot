import streamlit as st


def configure_page():

    st.set_page_config(
        page_title="AI Trading Copilot",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def show_header():

    st.title("📈 AI Trading Copilot")

    st.success("🟢 Market Data Connected")

    st.divider()