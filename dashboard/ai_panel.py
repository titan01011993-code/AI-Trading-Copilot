import streamlit as st

from ai.decision_engine import DecisionEngine


def render(df, symbol: str = "UNKNOWN"):
    """
    Render AI Trade Setup panel in Streamlit dashboard.
    
    Args:
        df: DataFrame with OHLC and indicators
        symbol: Stock symbol for analysis
    """
    decision = DecisionEngine.analyze(df, symbol=symbol)

    st.subheader("🤖 AI Trade Setup")

    # Signal and Confidence
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Signal", decision.signal)
    with col2:
        st.metric("Confidence", f"{decision.confidence:.1f}%")

    # Price Levels
    st.write("### Price Levels")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Entry", f"₹ {decision.entry:.2f}")
    with col2:
        st.metric("Stop Loss", f"₹ {decision.stop_loss:.2f}")
    with col3:
        st.metric("Risk", f"₹ {abs(decision.entry - decision.stop_loss):.2f}")

    # Targets
    st.write("### Targets")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Target 1", f"₹ {decision.target1:.2f}")
    with col2:
        st.metric("Target 2", f"₹ {decision.target2:.2f}")
    with col3:
        st.metric("Risk : Reward", f"1 : {decision.risk_reward_ratio:.2f}")

    # Analysis Reasons
    st.write("### Analysis")
    for reason in decision.reasons:
        st.success(f"✓ {reason}")
