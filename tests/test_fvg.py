from market.historical import HistoricalService

from indicators.fair_value_gap import FairValueGapIndicator

history = HistoricalService()

df = history.load("NIFTY")

df = FairValueGapIndicator.calculate(df)

print(
    df[
        [
            "datetime",
            "FVG_TYPE",
            "FVG_TOP",
            "FVG_BOTTOM",
            "FVG_VALID",
        ]
    ]
    .dropna(subset=["FVG_TYPE"])
    .tail(30)
)