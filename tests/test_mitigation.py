from market.historical import HistoricalService

from indicators.swing import SwingIndicator
from indicators.bos import BOSIndicator
from indicators.order_block import OrderBlockIndicator
from indicators.mitigation import MitigationIndicator

history = HistoricalService()

df = history.load("NIFTY")

df = SwingIndicator.calculate(df)
df = BOSIndicator.calculate(df)
df = OrderBlockIndicator.calculate(df)
df = MitigationIndicator.calculate(df)

print(
    df[
        [
            "datetime",
            "MITIGATED",
            "MITIGATION_PRICE",
        ]
    ][df["MITIGATED"]]
)