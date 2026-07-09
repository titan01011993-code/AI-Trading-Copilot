from market.historical import HistoricalService
from indicators.volume import VolumeIndicator

history = HistoricalService()

df = history.load("RELIANCE")

df = VolumeIndicator.calculate(df)

print(
    df[
        [
            "datetime",
            "open",
            "close",
            "volume",
            "VOLUME_COLOR",
        ]
    ].tail()
)