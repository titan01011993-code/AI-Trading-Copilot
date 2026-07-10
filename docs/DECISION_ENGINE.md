# DecisionEngine - AI Trading Decision Engine

## Overview

The `DecisionEngine` is the core decision-making component of the AI Trading Copilot. It analyzes technical indicators and market structure to generate **production-grade trading signals** with precise entry points, stop losses, targets, and risk-reward ratios.

## Architecture

### Input Requirements

The DecisionEngine requires a pandas DataFrame with the following columns:

```python
Required Columns:
- EMA_20      : 20-period Exponential Moving Average
- EMA_50      : 50-period Exponential Moving Average
- EMA_200     : 200-period Exponential Moving Average
- RSI         : Relative Strength Index (0-100)
- MACD        : MACD line value
- MACD_SIGNAL : MACD signal line value
- ATR         : Average True Range (volatility measure)
- close       : Closing price
```

### Output: DecisionOutput Dataclass

The engine returns a `DecisionOutput` object with:

```python
@dataclass
class DecisionOutput:
    symbol: str                      # Stock symbol
    signal: str                      # BUY, SELL, or HOLD
    confidence: float                # 0-100 score
    entry: float                     # Entry price
    stop_loss: float                 # Stop loss price
    target1: float                   # First target
    target2: float                   # Second target
    risk_reward_ratio: float         # RR ratio
    reasons: List[str]               # Analysis explanations
    timestamp: datetime              # Analysis timestamp
```

## Signal Generation Logic

### 1. Trend Analysis (EMA Alignment)
- **Bullish**: EMA_20 > EMA_50 > EMA_200 → +40 score
- **Bearish**: Otherwise → -40 score

### 2. Momentum Analysis (RSI)
- **Oversold** (RSI < 30): +30 score
- **Overbought** (RSI > 70): -30 score
- **Neutral** (30 ≤ RSI ≤ 70): 0 score

### 3. MACD Analysis
- **Bullish** (MACD > MACD_SIGNAL): +30 score
- **Bearish** (MACD ≤ MACD_SIGNAL): -30 score

### 4. Final Signal Decision
```
Score ≥ 40  → BUY
Score ≤ -40 → SELL
-40 < Score < 40 → HOLD
```

### 5. Confidence Calculation
```
confidence = min(abs(score), 100)
```

## Price Levels Calculation

All levels are calculated using **ATR (Average True Range)**:

```
entry = current_close_price

For BUY/SELL signals:
  stop_loss = entry - (1.5 × ATR)
  target1   = entry + (2.0 × ATR)
  target2   = entry + (4.0 × ATR)

For HOLD:
  stop_loss = target1 = target2 = entry (no position)
```

## Risk-Reward Ratio

```
risk = |entry - stop_loss|
reward = |target1 - entry|
RR_ratio = reward / risk

Example: 1:2 RR means for every ₹1 risked, you can make ₹2
```

## Usage Examples

### Basic Usage

```python
from market.historical import HistoricalService
from indicators.ema import EMAIndicator
from indicators.rsi import RSIIndicator
from indicators.macd import MACDIndicator
from indicators.atr import ATRIndicator
from ai.decision_engine import DecisionEngine

# Load and prepare data
history = HistoricalService()
df = history.load("RELIANCE")

# Calculate indicators
df = EMAIndicator.calculate(df)
df = RSIIndicator.calculate(df)
df = MACDIndicator.calculate(df)
df = ATRIndicator.calculate(df)

# Analyze
decision = DecisionEngine.analyze(df, symbol="RELIANCE")

print(f"Signal: {decision.signal}")
print(f"Confidence: {decision.confidence:.1f}%")
print(f"Entry: ₹{decision.entry:.2f}")
print(f"Stop Loss: ₹{decision.stop_loss:.2f}")
print(f"Target 1: ₹{decision.target1:.2f}")
print(f"Target 2: ₹{decision.target2:.2f}")
print(f"Risk-Reward: 1:{decision.risk_reward_ratio:.2f}")
```

### With Dashboard Integration

```python
from dashboard.ai_panel import render

# In Streamlit app
render(df, symbol="RELIANCE")
```

## Error Handling

The engine validates all inputs and raises descriptive errors:

```python
# Missing columns
DecisionEngine.analyze(df)
# ValueError: Missing required columns: ['EMA_20', 'EMA_50', ...]

# Empty dataframe
DecisionEngine.analyze(pd.DataFrame())
# ValueError: DataFrame is empty
```

## Configuration

### Thresholds (Tunable)

These can be modified in the DecisionEngine class:

```python
BUY_THRESHOLD = 40        # Score threshold for BUY
SELL_THRESHOLD = -40      # Score threshold for SELL

# ATR Multipliers for level calculation
STOP_LOSS_ATR_MULTIPLE = 1.5
TARGET1_ATR_MULTIPLE = 2.0
TARGET2_ATR_MULTIPLE = 4.0
```

## Testing

Comprehensive unit tests are in `tests/test_decision_engine.py`:

```bash
# Run all DecisionEngine tests
pytest tests/test_decision_engine.py -v

# Run specific test class
pytest tests/test_decision_engine.py::TestDecisionEngineSignals -v

# Run with coverage
pytest tests/test_decision_engine.py --cov=ai.decision_engine
```

Test Coverage:
- ✅ Input validation
- ✅ Signal generation (BUY, SELL, HOLD)
- ✅ Price level calculation
- ✅ Risk-reward ratio
- ✅ Confidence scoring
- ✅ Edge cases (oversold, overbought, etc.)
- ✅ DataClass conversion to Signal

## Production Checklist

- ✅ Type hints on all methods
- ✅ Input validation with descriptive errors
- ✅ Immutable dataclass with slots
- ✅ Unit test coverage (20+ tests)
- ✅ Backward compatibility maintained
- ✅ Modular design (easy to extend)
- ✅ Clear documentation
- ✅ No placeholder code

## Future Enhancements

- [ ] Multi-timeframe analysis integration (4-hour, daily context)
- [ ] Volume profile analysis
- [ ] Smart money concepts (BOS, CHOCH, Order Blocks)
- [ ] Machine learning confidence scoring
- [ ] Real-time alert system
- [ ] Trade performance tracking

## Integration Points

### With Other Engines (Upcoming)

```python
# Will integrate with:
from trade_planner import TradePlanner
from risk_engine import RiskEngine
from signal_engine import SignalEngine
from confidence_engine import ConfidenceEngine

# Decision → TradePlanner → RiskEngine → Execution
```

### With Dashboard

Current integration: `dashboard/ai_panel.py` renders DecisionOutput
- Signal indicator
- Confidence gauge
- Price levels display
- Risk-reward ratio
- Analysis reasons

---

**Status:** ✅ Production Ready (v1.0)  
**Last Updated:** 2026-07-10  
**Author:** Copilot AI
