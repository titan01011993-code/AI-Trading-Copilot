from market.historical import HistoricalService
from indicators.rsi import RSIIndicator

history = HistoricalService()

df = history.load("RELIANCE")

df = RSIIndicator.calculate(df)

print(df[["datetime", "close", "RSI"]].tail())