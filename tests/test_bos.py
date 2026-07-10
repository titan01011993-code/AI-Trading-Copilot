from market.historical import HistoricalService

from indicators.swing import SwingIndicator
from indicators.bos import BOSIndicator

history = HistoricalService()

df = history.load("NIFTY")

df = SwingIndicator.calculate(df)
df = BOSIndicator.calculate(df)

print(
    df[
        [
            "datetime",
            "close",
            "SWING_HIGH",
            "SWING_LOW",
            "BOS",
            "BOS_DIRECTION",
        ]
    ].tail(40)
)