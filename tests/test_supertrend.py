from market.historical import HistoricalService
from indicators.supertrend import SuperTrendIndicator

history = HistoricalService()

df = history.load("NIFTY")

df = SuperTrendIndicator.calculate(df)

print(
    df[
        [
            "datetime",
            "close",
            "SUPERTREND",
            "SUPERTREND_DIRECTION",
        ]
    ].tail(20)
)