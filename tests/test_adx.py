from market.historical import HistoricalService
from indicators.adx import ADXIndicator

history = HistoricalService()

df = history.load("NIFTY")

df = ADXIndicator.calculate(df)

print(
    df[
        [
            "datetime",
            "PLUS_DI",
            "MINUS_DI",
            "ADX",
            "ADX_SIGNAL",
            "TREND_STRENGTH",
        ]
    ].tail(20)
)