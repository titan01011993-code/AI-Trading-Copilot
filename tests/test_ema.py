from market.historical import HistoricalService
from indicators.ema import EMAIndicator

history = HistoricalService()

df = history.load("RELIANCE")

df = EMAIndicator.calculate(df)

print(df.tail())