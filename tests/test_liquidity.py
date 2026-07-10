from market.historical import HistoricalService

from indicators.swing import SwingIndicator
from indicators.liquidity import LiquidityIndicator

history = HistoricalService()

df = history.load("NIFTY")

df = SwingIndicator.calculate(df)
df = LiquidityIndicator.calculate(df)

print(
    df[
        [
            "datetime",
            "high",
            "low",
            "EQUAL_HIGH",
            "EQUAL_LOW",
            "BUY_SIDE_LIQUIDITY",
            "SELL_SIDE_LIQUIDITY",
        ]
    ][
        (df["EQUAL_HIGH"]) | (df["EQUAL_LOW"])
    ]
)