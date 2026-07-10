from market.historical import HistoricalService

from indicators.swing import SwingIndicator
from indicators.bos import BOSIndicator
from indicators.order_block import OrderBlockIndicator

history = HistoricalService()

df = history.load("NIFTY")

df = SwingIndicator.calculate(df)
df = BOSIndicator.calculate(df)
df = OrderBlockIndicator.calculate(df)

print(
    df[
        [
            "datetime",
            "BOS_DIRECTION",
            "OB_TYPE",
            "OB_HIGH",
            "OB_LOW",
            "OB_VALID",
        ]
    ].dropna(subset=["OB_TYPE"]).tail(20)
)