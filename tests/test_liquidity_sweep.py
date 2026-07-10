from market.historical import HistoricalService

from indicators.swing import SwingIndicator
from indicators.liquidity import LiquidityIndicator
from indicators.liquidity_sweep import LiquiditySweepIndicator

history = HistoricalService()

df = history.load("NIFTY")

df = SwingIndicator.calculate(df)
df = LiquidityIndicator.calculate(df)
df = LiquiditySweepIndicator.calculate(df)

print(
    df[
        [
            "datetime",
            "high",
            "low",
            "close",
            "SWEEP",
            "SWEEP_DIRECTION",
            "SWEEP_LEVEL",
        ]
    ][df["SWEEP"]]
)