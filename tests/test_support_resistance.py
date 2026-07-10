from market.historical import HistoricalService
from indicators.swing import SwingIndicator
from indicators.support_resistance import SupportResistanceIndicator

history = HistoricalService()

df = history.load("NIFTY")

df = SwingIndicator.calculate(df)
df = SupportResistanceIndicator.calculate(df)

print(
    df[
        [
            "datetime",
            "close",
            "SUPPORT",
            "RESISTANCE",
        ]
    ].tail(30)
)