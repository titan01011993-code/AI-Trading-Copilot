import pytest
import pandas as pd
from datetime import datetime, timedelta
from ai.decision_engine import DecisionEngine
from core.enums import Recommendation


@pytest.fixture
def sample_bullish_df():
    """Create a sample dataframe with bullish signals."""
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    data = {
        'timestamp': dates,
        'open': [100 + i*0.5 for i in range(100)],
        'high': [102 + i*0.5 for i in range(100)],
        'low': [99 + i*0.5 for i in range(100)],
        'close': [101 + i*0.5 for i in range(100)],
        'volume': [1000000] * 100,
        'EMA_20': [100 + i*0.5 for i in range(100)],
        'EMA_50': [99 + i*0.4 for i in range(100)],
        'EMA_200': [98 + i*0.3 for i in range(100)],
        'RSI': [45 + i*0.1 for i in range(100)],
        'MACD': [0.5 + i*0.01 for i in range(100)],
        'MACD_SIGNAL': [0.4 + i*0.01 for i in range(100)],
        'ATR': [2.0] * 100,
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_bearish_df():
    """Create a sample dataframe with bearish signals."""
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    data = {
        'timestamp': dates,
        'open': [100 - i*0.5 for i in range(100)],
        'high': [102 - i*0.5 for i in range(100)],
        'low': [99 - i*0.5 for i in range(100)],
        'close': [101 - i*0.5 for i in range(100)],
        'volume': [1000000] * 100,
        'EMA_20': [99 - i*0.5 for i in range(100)],
        'EMA_50': [100 - i*0.4 for i in range(100)],
        'EMA_200': [101 - i*0.3 for i in range(100)],
        'RSI': [55 - i*0.1 for i in range(100)],
        'MACD': [0.4 - i*0.01 for i in range(100)],
        'MACD_SIGNAL': [0.5 - i*0.01 for i in range(100)],
        'ATR': [2.0] * 100,
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_neutral_df():
    """Create a sample dataframe with neutral signals."""
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    data = {
        'timestamp': dates,
        'open': [100] * 100,
        'high': [102] * 100,
        'low': [99] * 100,
        'close': [100.5] * 100,
        'volume': [1000000] * 100,
        'EMA_20': [100.5] * 100,
        'EMA_50': [100.5] * 100,
        'EMA_200': [100.5] * 100,
        'RSI': [50] * 100,
        'MACD': [0.45] * 100,
        'MACD_SIGNAL': [0.45] * 100,
        'ATR': [2.0] * 100,
    }
    return pd.DataFrame(data)


class TestDecisionEngineValidation:
    """Test DecisionEngine input validation."""

    def test_missing_required_columns(self):
        """Should raise error if required columns are missing."""
        df = pd.DataFrame({'close': [100, 101, 102]})
        
        with pytest.raises(ValueError, match="Missing required columns"):
            DecisionEngine.analyze(df)

    def test_empty_dataframe(self):
        """Should raise error if dataframe is empty."""
        df = pd.DataFrame(columns=[
            'EMA_20', 'EMA_50', 'EMA_200', 'RSI', 'MACD', 'MACD_SIGNAL', 'ATR', 'close'
        ])
        
        with pytest.raises(ValueError, match="DataFrame is empty"):
            DecisionEngine.analyze(df)

    def test_valid_dataframe(self, sample_bullish_df):
        """Should not raise error with valid dataframe."""
        result = DecisionEngine.analyze(sample_bullish_df, symbol="TEST")
        assert result is not None
        assert result.symbol == "TEST"


class TestDecisionEngineSignals:
    """Test DecisionEngine signal generation."""

    def test_bullish_signal(self, sample_bullish_df):
        """Should generate BUY signal when conditions are bullish."""
        result = DecisionEngine.analyze(sample_bullish_df, symbol="BULLISH")
        
        assert result.signal == Recommendation.BUY.value
        assert result.confidence > 0
        assert len(result.reasons) > 0

    def test_bearish_signal(self, sample_bearish_df):
        """Should generate SELL signal when conditions are bearish."""
        result = DecisionEngine.analyze(sample_bearish_df, symbol="BEARISH")
        
        assert result.signal == Recommendation.SELL.value
        assert result.confidence > 0

    def test_neutral_signal(self, sample_neutral_df):
        """Should generate HOLD signal when conditions are neutral."""
        result = DecisionEngine.analyze(sample_neutral_df, symbol="NEUTRAL")
        
        assert result.signal == Recommendation.HOLD.value


class TestDecisionEngineLevels:
    """Test entry, stop loss, and target calculation."""

    def test_buy_levels(self, sample_bullish_df):
        """BUY signal should have proper entry, stop, and targets."""
        result = DecisionEngine.analyze(sample_bullish_df)
        
        # For BUY: stop < entry < target1 < target2
        assert result.stop_loss < result.entry
        assert result.entry < result.target1
        assert result.target1 < result.target2

    def test_sell_levels(self, sample_bearish_df):
        """SELL signal should have proper entry, stop, and targets."""
        result = DecisionEngine.analyze(sample_bearish_df)
        
        # Stop loss calculation should be consistent
        assert result.stop_loss is not None
        assert result.target1 is not None
        assert result.target2 is not None

    def test_hold_levels(self, sample_neutral_df):
        """HOLD signal should have entry as all levels."""
        result = DecisionEngine.analyze(sample_neutral_df)
        
        assert result.stop_loss == result.entry
        assert result.target1 == result.entry
        assert result.target2 == result.entry

    def test_level_precision(self, sample_bullish_df):
        """All price levels should be rounded to 2 decimals."""
        result = DecisionEngine.analyze(sample_bullish_df)
        
        assert len(str(result.entry).split('.')[-1]) <= 2
        assert len(str(result.stop_loss).split('.')[-1]) <= 2
        assert len(str(result.target1).split('.')[-1]) <= 2
        assert len(str(result.target2).split('.')[-1]) <= 2


class TestDecisionEngineRiskReward:
    """Test risk-reward ratio calculation."""

    def test_risk_reward_ratio(self, sample_bullish_df):
        """Should calculate valid risk-reward ratio."""
        result = DecisionEngine.analyze(sample_bullish_df)
        
        if result.signal == Recommendation.BUY.value:
            # RR should be positive for valid trade
            assert result.risk_reward_ratio > 0

    def test_zero_risk_handling(self, sample_neutral_df):
        """Should handle zero risk (entry == stop loss)."""
        result = DecisionEngine.analyze(sample_neutral_df)
        
        # HOLD should have zero risk-reward
        assert result.risk_reward_ratio == 0.0


class TestDecisionEngineConfidence:
    """Test confidence scoring."""

    def test_confidence_range(self, sample_bullish_df):
        """Confidence should be between 0 and 100."""
        result = DecisionEngine.analyze(sample_bullish_df)
        
        assert 0 <= result.confidence <= 100

    def test_confidence_strong_bullish(self, sample_bullish_df):
        """Strong bullish signal should have high confidence."""
        result = DecisionEngine.analyze(sample_bullish_df)
        
        if result.signal == Recommendation.BUY.value:
            assert result.confidence > 40


class TestDecisionEngineReasons:
    """Test reasoning explanations."""

    def test_reasons_populated(self, sample_bullish_df):
        """Should provide reasons for decision."""
        result = DecisionEngine.analyze(sample_bullish_df)
        
        assert len(result.reasons) > 0
        assert all(isinstance(r, str) for r in result.reasons)

    def test_reasons_specific(self, sample_bullish_df):
        """Reasons should be specific and meaningful."""
        result = DecisionEngine.analyze(sample_bullish_df)
        
        reason_text = " ".join(result.reasons)
        # Should contain technical indicator references
        assert any(indicator in reason_text for indicator in ["EMA", "RSI", "MACD"])


class TestDecisionOutputDataclass:
    """Test DecisionOutput dataclass functionality."""

    def test_decision_output_attributes(self, sample_bullish_df):
        """DecisionOutput should have all required attributes."""
        result = DecisionEngine.analyze(sample_bullish_df, symbol="TEST")
        
        assert hasattr(result, 'symbol')
        assert hasattr(result, 'signal')
        assert hasattr(result, 'confidence')
        assert hasattr(result, 'entry')
        assert hasattr(result, 'stop_loss')
        assert hasattr(result, 'target1')
        assert hasattr(result, 'target2')
        assert hasattr(result, 'risk_reward_ratio')
        assert hasattr(result, 'reasons')
        assert hasattr(result, 'timestamp')

    def test_decision_output_to_signal(self, sample_bullish_df):
        """DecisionOutput should convert to Signal dataclass."""
        decision = DecisionEngine.analyze(sample_bullish_df, symbol="TEST")
        signal = decision.to_signal("UPTREND")
        
        assert signal.symbol == "TEST"
        assert signal.trend == "UPTREND"
        assert signal.recommendation == decision.signal
        assert signal.confidence == decision.confidence
        assert signal.stop_loss == decision.stop_loss


class TestDecisionEngineEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_rsi_oversold(self):
        """Should detect RSI oversold condition."""
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        data = {
            'timestamp': dates,
            'open': [100] * 100,
            'high': [102] * 100,
            'low': [99] * 100,
            'close': [100] * 100,
            'volume': [1000000] * 100,
            'EMA_20': [101] * 100,
            'EMA_50': [100] * 100,
            'EMA_200': [99] * 100,
            'RSI': [25] * 100,  # Oversold
            'MACD': [0.5] * 100,
            'MACD_SIGNAL': [0.4] * 100,
            'ATR': [2.0] * 100,
        }
        df = pd.DataFrame(data)
        result = DecisionEngine.analyze(df)
        
        assert "Oversold" in " ".join(result.reasons)

    def test_rsi_overbought(self):
        """Should detect RSI overbought condition."""
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        data = {
            'timestamp': dates,
            'open': [100] * 100,
            'high': [102] * 100,
            'low': [99] * 100,
            'close': [100] * 100,
            'volume': [1000000] * 100,
            'EMA_20': [99] * 100,
            'EMA_50': [100] * 100,
            'EMA_200': [101] * 100,
            'RSI': [75] * 100,  # Overbought
            'MACD': [0.4] * 100,
            'MACD_SIGNAL': [0.5] * 100,
            'ATR': [2.0] * 100,
        }
        df = pd.DataFrame(data)
        result = DecisionEngine.analyze(df)
        
        assert "Overbought" in " ".join(result.reasons)

    def test_with_symbol_name(self, sample_bullish_df):
        """Should accept and store symbol name."""
        result = DecisionEngine.analyze(sample_bullish_df, symbol="RELIANCE")
        assert result.symbol == "RELIANCE"

    def test_default_symbol(self, sample_bullish_df):
        """Should use default symbol if not provided."""
        result = DecisionEngine.analyze(sample_bullish_df)
        assert result.symbol == "UNKNOWN"
