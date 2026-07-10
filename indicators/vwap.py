import numpy as np
import pandas as pd


class VWAPIndicator:
    """
    Volume Weighted Average Price

    Outputs
    -------
    VWAP
    VWAP_DISTANCE
    VWAP_SIGNAL
    """

    @staticmethod
    def calculate(df: pd.DataFrame) -> pd.DataFrame:

        data = df.copy()

        # Typical Price
        tp = (
            data["high"]
            + data["low"]
            + data["close"]
        ) / 3

        # Cumulative Price * Volume
        cumulative_pv = (tp * data["volume"]).cumsum()

        # Cumulative Volume
        cumulative_volume = data["volume"].cumsum()

        # VWAP
        data["VWAP"] = cumulative_pv / cumulative_volume

        # Distance (%)
        data["VWAP_DISTANCE"] = (
            (data["close"] - data["VWAP"])
            / data["VWAP"]
        ) * 100

        # Signal
        data["VWAP_SIGNAL"] = np.where(
            data["close"] >= data["VWAP"],
            "Bullish",
            "Bearish"
        )

        return data