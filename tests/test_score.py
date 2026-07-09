from market.historical import HistoricalService

from indicators.ema import EMAIndicator
from indicators.rsi import RSIIndicator
from indicators.macd import MACDIndicator
from indicators.volume import VolumeIndicator

from ai.scoring import ScoringEngine

history = HistoricalService()

df = history.load("RELIANCE")

df = EMAIndicator.calculate(df)
df = RSIIndicator.calculate(df)
df = MACDIndicator.calculate(df)
df = VolumeIndicator.calculate(df)

last = df.iloc[-1]

print("EMA20 :", last["EMA_20"])
print("EMA50 :", last["EMA_50"])
print("EMA200:", last["EMA_200"])

print("RSI:", last["RSI"])

print("MACD:", last["MACD"])
print("SIGNAL:", last["MACD_SIGNAL"])

print("Volume:", last["volume"])
print("20 Day Avg:", df["volume"].tail(20).mean())

score, reasons = ScoringEngine.technical_score(df)

print("Technical Score:", score)

print("\nReasons:")

for r in reasons:
    print("-", r)