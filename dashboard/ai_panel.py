import streamlit as st

from ai.decision_engine import DecisionEngine


def render(df):

    result = DecisionEngine.analyze(df)

    st.subheader("🤖 AI Trade Setup")

    st.metric("Signal", result["signal"])

    st.metric("Confidence", f"{result['confidence']}%")

    st.metric("Entry", f"₹ {result['entry']}")

    st.metric("Stop Loss", f"₹ {result['stop']}")

    st.metric("Target 1", f"₹ {result['target1']}")

    st.metric("Target 2", f"₹ {result['target2']}")

    st.metric("Risk : Reward", f"1 : {result['rr']}")

    st.write("### Reasons")

    for reason in result["reasons"]:
        st.success(reason)