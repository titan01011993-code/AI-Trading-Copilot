from market.historical import HistoricalService
from indicators.swing import SwingIndicator


history = HistoricalService()

df = history.load("NIFTY")

df = SwingIndicator.calculate(df)

print(
    df[
        [
            "datetime",
            "high",
            "low",
            "SWING_HIGH",
            "SWING_LOW",
            "SWING_HIGH_PRICE",
            "SWING_LOW_PRICE",
        ]
    ].tail(30)
)