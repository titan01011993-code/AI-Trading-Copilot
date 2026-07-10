from market.historical import HistoricalService
from indicators.master_pipeline import MasterPipeline
from features.feature_engine import FeatureEngine

history = HistoricalService()

df = history.load("NIFTY")

df = MasterPipeline.calculate(df)

df = FeatureEngine.calculate(df)

print(df[
[
"EMA_ALIGNMENT",
"EMA_DISTANCE",
"PRICE_ABOVE_EMA20",
"RSI_STRENGTH",
"MACD_DISTANCE",
"MACD_BULLISH",
"VOLUME_RATIO",
"HIGH_VOLUME",
"ATR_PERCENT"
]
].tail())