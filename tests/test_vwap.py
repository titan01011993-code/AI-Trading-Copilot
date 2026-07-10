from market.historical import HistoricalService
from indicators.vwap import VWAPIndicator

history = HistoricalService()

df = history.load("NIFTY")

df = VWAPIndicator.calculate(df)

print(
    df[
        [
            "datetime",
            "close",
            "VWAP",
            "VWAP_DISTANCE",
            "VWAP_SIGNAL",
        ]
    ].tail(20)
)