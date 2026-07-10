from market.historical import HistoricalService

from indicators.swing import SwingIndicator
from indicators.bos import BOSIndicator
from indicators.choch import CHOCHIndicator


history = HistoricalService()

df = history.load("NIFTY")

df = SwingIndicator.calculate(df)
df = BOSIndicator.calculate(df)
df = CHOCHIndicator.calculate(df)

print(
    df[
        [
            "datetime",
            "close",
            "BOS",
            "BOS_DIRECTION",
            "CHOCH",
            "CHOCH_DIRECTION",
        ]
    ].tail(50)
)