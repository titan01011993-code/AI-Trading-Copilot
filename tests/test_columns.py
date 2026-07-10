from market.historical import HistoricalService
from indicators.ema import EMAIndicator
from indicators.rsi import RSIIndicator
from indicators.macd import MACDIndicator
from indicators.atr import ATRIndicator

history = HistoricalService()

df = history.load("^NSEI")

df = EMAIndicator.calculate(df)

df = RSIIndicator.calculate(df)

df = MACDIndicator.calculate(df)

df = ATRIndicator.calculate(df)

print(df.columns.tolist())