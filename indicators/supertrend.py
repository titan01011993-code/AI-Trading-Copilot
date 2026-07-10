import numpy as np
import pandas as pd


class SuperTrendIndicator:
    """
    SuperTrend Indicator

    Outputs:
        SUPERTREND
        SUPERTREND_DIRECTION
    """

    @staticmethod
    def calculate(
        df: pd.DataFrame,
        period: int = 10,
        multiplier: float = 3.0,
    ) -> pd.DataFrame:

        data = df.copy()

        # --------------------------
        # ATR
        # --------------------------

        high = data["high"]
        low = data["low"]
        close = data["close"]

        prev_close = close.shift(1)

        tr = pd.concat(
            [
                high - low,
                (high - prev_close).abs(),
                (low - prev_close).abs(),
            ],
            axis=1,
        ).max(axis=1)

        atr = tr.ewm(
            alpha=1 / period,
            adjust=False,
        ).mean()

        # --------------------------
        # Basic Bands
        # --------------------------

        hl2 = (high + low) / 2

        upperband = hl2 + multiplier * atr
        lowerband = hl2 - multiplier * atr

        final_upper = upperband.copy()
        final_lower = lowerband.copy()

        for i in range(1, len(data)):

            if (
                upperband.iloc[i] < final_upper.iloc[i - 1]
                or close.iloc[i - 1] > final_upper.iloc[i - 1]
            ):
                final_upper.iloc[i] = upperband.iloc[i]
            else:
                final_upper.iloc[i] = final_upper.iloc[i - 1]

            if (
                lowerband.iloc[i] > final_lower.iloc[i - 1]
                or close.iloc[i - 1] < final_lower.iloc[i - 1]
            ):
                final_lower.iloc[i] = lowerband.iloc[i]
            else:
                final_lower.iloc[i] = final_lower.iloc[i - 1]

        supertrend = np.zeros(len(data))
        direction = ["Bullish"] * len(data)

        supertrend[0] = final_lower.iloc[0]

        for i in range(1, len(data)):

            if close.iloc[i] > final_upper.iloc[i - 1]:

                direction[i] = "Bullish"

            elif close.iloc[i] < final_lower.iloc[i - 1]:

                direction[i] = "Bearish"

            else:

                direction[i] = direction[i - 1]

            if direction[i] == "Bullish":
                supertrend[i] = final_lower.iloc[i]
            else:
                supertrend[i] = final_upper.iloc[i]

        data["SUPERTREND"] = supertrend
        data["SUPERTREND_DIRECTION"] = direction

        return data