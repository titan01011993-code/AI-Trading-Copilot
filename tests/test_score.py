from market.historical import HistoricalService

from indicators.ema import EMAIndicator
from indicators.rsi import RSIIndicator
from indicators.macd import MACDIndicator
from indicators.volume import VolumeIndicator
from indicators.atr import ATRIndicator

from ai.decision_engine import DecisionEngine

history = HistoricalService()

df = history.load("RELIANCE")

df = EMAIndicator.calculate(df)
df = RSIIndicator.calculate(df)
df = MACDIndicator.calculate(df)
df = VolumeIndicator.calculate(df)
df = ATRIndicator.calculate(df)

last = df.iloc[-1]

print("=" * 60)
print("TECHNICAL INDICATORS")
print("=" * 60)

print(f"EMA20 : {last['EMA_20']:.2f}")
print(f"EMA50 : {last['EMA_50']:.2f}")
print(f"EMA200: {last['EMA_200']:.2f}")

print(f"\nRSI: {last['RSI']:.2f}")

print(f"\nMACD: {last['MACD']:.4f}")
print(f"SIGNAL: {last['MACD_SIGNAL']:.4f}")

print(f"\nATR: {last['ATR']:.2f}")
print(f"Volume: {last['volume']:.0f}")
print(f"20 Day Avg Vol: {df['volume'].tail(20).mean():.0f}")

# DecisionEngine analysis
print("\n" + "=" * 60)
print("DECISION ENGINE ANALYSIS")
print("=" * 60)

decision = DecisionEngine.analyze(df, symbol="RELIANCE")

print(f"\nSignal: {decision.signal}")
print(f"Confidence: {decision.confidence:.1f}%")
print(f"Entry: {decision.entry:.2f}")
print(f"Stop Loss: {decision.stop_loss:.2f}")
print(f"Target 1: {decision.target1:.2f}")
print(f"Target 2: {decision.target2:.2f}")
print(f"Risk-Reward Ratio: {decision.risk_reward_ratio:.2f}")

print("\nReasons:")
for reason in decision.reasons:
    print(f"  • {reason}")
