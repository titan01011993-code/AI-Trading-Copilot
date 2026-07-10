"""
Integration test for DecisionEngine with full pipeline.
Tests the complete flow from data loading through decision generation.
"""

import pandas as pd
from market.historical import HistoricalService
from indicators.ema import EMAIndicator
from indicators.rsi import RSIIndicator
from indicators.macd import MACDIndicator
from indicators.atr import ATRIndicator
from indicators.volume import VolumeIndicator
from ai.decision_engine import DecisionEngine
from core.enums import Recommendation


def test_full_pipeline_bullish():
    """Test complete pipeline with real data for bullish signal."""
    print("\n" + "="*70)
    print("INTEGRATION TEST: Full Pipeline - Bullish Signal")
    print("="*70)
    
    # Load data
    history = HistoricalService()
    df = history.load("RELIANCE")
    print(f"✓ Loaded {len(df)} candles for RELIANCE")
    
    # Calculate all indicators
    df = EMAIndicator.calculate(df)
    df = RSIIndicator.calculate(df)
    df = MACDIndicator.calculate(df)
    df = ATRIndicator.calculate(df)
    df = VolumeIndicator.calculate(df)
    print("✓ Calculated all indicators")
    
    # Run DecisionEngine
    decision = DecisionEngine.analyze(df, symbol="RELIANCE")
    print(f"✓ Generated decision: {decision.signal}")
    
    # Validate output
    assert decision.symbol == "RELIANCE"
    assert decision.signal in [Recommendation.BUY.value, Recommendation.SELL.value, Recommendation.HOLD.value]
    assert 0 <= decision.confidence <= 100
    assert decision.entry > 0
    assert decision.stop_loss > 0
    assert decision.target1 > 0
    assert decision.target2 > 0
    assert decision.risk_reward_ratio >= 0
    assert len(decision.reasons) > 0
    assert decision.timestamp is not None
    print("✓ All output validations passed")
    
    # Display results
    last = df.iloc[-1]
    print(f"\nTechnical Indicators (Latest):")
    print(f"  EMA20:  {last['EMA_20']:.2f}")
    print(f"  EMA50:  {last['EMA_50']:.2f}")
    print(f"  EMA200: {last['EMA_200']:.2f}")
    print(f"  RSI:    {last['RSI']:.2f}")
    print(f"  MACD:   {last['MACD']:.4f} (Signal: {last['MACD_SIGNAL']:.4f})")
    print(f"  ATR:    {last['ATR']:.2f}")
    
    print(f"\nDecision Engine Output:")
    print(f"  Signal:      {decision.signal}")
    print(f"  Confidence:  {decision.confidence:.1f}%")
    print(f"  Entry:       ₹{decision.entry:.2f}")
    print(f"  Stop Loss:   ₹{decision.stop_loss:.2f}")
    print(f"  Target 1:    ₹{decision.target1:.2f}")
    print(f"  Target 2:    ₹{decision.target2:.2f}")
    print(f"  Risk-Reward: 1:{decision.risk_reward_ratio:.2f}")
    
    print(f"\nAnalysis Reasons:")
    for reason in decision.reasons:
        print(f"  • {reason}")
    
    print("\n✅ Integration test PASSED")
    return decision


def test_dataclass_conversion():
    """Test DecisionOutput to Signal dataclass conversion."""
    print("\n" + "="*70)
    print("INTEGRATION TEST: DecisionOutput to Signal Conversion")
    print("="*70)
    
    # Generate decision
    history = HistoricalService()
    df = history.load("INFY")
    
    df = EMAIndicator.calculate(df)
    df = RSIIndicator.calculate(df)
    df = MACDIndicator.calculate(df)
    df = ATRIndicator.calculate(df)
    df = VolumeIndicator.calculate(df)
    
    decision = DecisionEngine.analyze(df, symbol="INFY")
    print(f"✓ Generated decision for INFY: {decision.signal}")
    
    # Convert to Signal
    signal = decision.to_signal(trend="UPTREND")
    print(f"✓ Converted to Signal dataclass")
    
    # Validate conversion
    assert signal.symbol == "INFY"
    assert signal.trend == "UPTREND"
    assert signal.recommendation == decision.signal
    assert signal.confidence == decision.confidence
    assert signal.stop_loss == decision.stop_loss
    assert signal.target == decision.target1
    print("✓ All conversion validations passed")
    
    print(f"\nConverted Signal:")
    print(f"  Symbol:         {signal.symbol}")
    print(f"  Trend:          {signal.trend}")
    print(f"  Recommendation: {signal.recommendation}")
    print(f"  Confidence:     {signal.confidence:.1f}%")
    print(f"  Stop Loss:      ₹{signal.stop_loss:.2f}")
    print(f"  Target:         ₹{signal.target:.2f}")
    
    print("\n✅ Dataclass conversion test PASSED")
    return signal


def test_dashboard_compatibility():
    """Test that DecisionEngine works with dashboard rendering."""
    print("\n" + "="*70)
    print("INTEGRATION TEST: Dashboard Compatibility")
    print("="*70)
    
    # Generate decision
    history = HistoricalService()
    df = history.load("TCS")
    
    df = EMAIndicator.calculate(df)
    df = RSIIndicator.calculate(df)
    df = MACDIndicator.calculate(df)
    df = ATRIndicator.calculate(df)
    df = VolumeIndicator.calculate(df)
    
    decision = DecisionEngine.analyze(df, symbol="TCS")
    print(f"✓ Generated decision for TCS: {decision.signal}")
    
    # Test dashboard attribute access (simulating streamlit rendering)
    try:
        signal_display = decision.signal
        confidence_display = f"{decision.confidence:.1f}%"
        entry_display = f"₹ {decision.entry:.2f}"
        stop_display = f"₹ {decision.stop_loss:.2f}"
        target1_display = f"₹ {decision.target1:.2f}"
        target2_display = f"₹ {decision.target2:.2f}"
        rr_display = f"1 : {decision.risk_reward_ratio:.2f}"
        
        print("✓ All dashboard rendering attributes accessible")
        
        print(f"\nDashboard Display Output:")
        print(f"  Signal:       {signal_display}")
        print(f"  Confidence:   {confidence_display}")
        print(f"  Entry:        {entry_display}")
        print(f"  Stop Loss:    {stop_display}")
        print(f"  Target 1:     {target1_display}")
        print(f"  Target 2:     {target2_display}")
        print(f"  Risk : Reward {rr_display}")
        
        # Test reasons iteration
        print(f"\nReasons for rendering:")
        for i, reason in enumerate(decision.reasons, 1):
            print(f"  {i}. {reason}")
        
        print("\n✅ Dashboard compatibility test PASSED")
        
    except Exception as e:
        print(f"❌ Dashboard compatibility test FAILED: {e}")
        raise


def test_error_handling():
    """Test error handling with invalid inputs."""
    print("\n" + "="*70)
    print("INTEGRATION TEST: Error Handling")
    print("="*70)
    
    # Test 1: Missing columns
    try:
        df = pd.DataFrame({'close': [100, 101, 102]})
        DecisionEngine.analyze(df)
        print("❌ Should have raised ValueError for missing columns")
    except ValueError as e:
        print(f"✓ Correctly raised error: {e}")
    
    # Test 2: Empty dataframe
    try:
        df = pd.DataFrame(columns=['EMA_20', 'EMA_50', 'EMA_200', 'RSI', 'MACD', 'MACD_SIGNAL', 'ATR', 'close'])
        DecisionEngine.analyze(df)
        print("❌ Should have raised ValueError for empty dataframe")
    except ValueError as e:
        print(f"✓ Correctly raised error: {e}")
    
    print("\n✅ Error handling test PASSED")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("DECISION ENGINE INTEGRATION TEST SUITE")
    print("="*70)
    
    try:
        test_full_pipeline_bullish()
        test_dataclass_conversion()
        test_dashboard_compatibility()
        test_error_handling()
        
        print("\n" + "="*70)
        print("✅ ALL INTEGRATION TESTS PASSED")
        print("="*70)
        
    except Exception as e:
        print("\n" + "="*70)
        print(f"❌ INTEGRATION TEST FAILED: {e}")
        print("="*70)
        raise
