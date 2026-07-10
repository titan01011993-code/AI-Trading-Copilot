from market.historical import HistoricalService
from indicators.pipeline import IndicatorPipeline
from indicators.technical_score import TechnicalScore

history = HistoricalService()

df = history.load("NIFTY")

df = IndicatorPipeline.calculate(df)

df = TechnicalScore.calculate(df)

print(
    df[
        [
            "datetime",
            "TREND_SCORE",
            "MOMENTUM_SCORE",
            "VOLUME_SCORE",
            "VOLATILITY_SCORE",
            "STRUCTURE_SCORE",
            "TECHNICAL_SCORE",
        ]
    ].tail(20)
)