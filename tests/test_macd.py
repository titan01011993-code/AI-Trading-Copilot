from market.historical import HistoricalService
from indicators.macd import MACDIndicator

history = HistoricalService()

df = history.load("RELIANCE")

df = MACDIndicator.calculate(df)

print(
    df[
        [
            "datetime",
            "close",
            "MACD",
            "MACD_SIGNAL",
            "MACD_HIST",
        ]
    ].tail()
)