import pandas as pd


class ATRIndicator:

    @staticmethod
    def calculate(
        df: pd.DataFrame,
        period: int = 14,
    ) -> pd.DataFrame:

        data = df.copy()

        high_low = data["high"] - data["low"]

        high_close = (
            data["high"] - data["close"].shift()
        ).abs()

        low_close = (
            data["low"] - data["close"].shift()
        ).abs()

        tr = pd.concat(
            [
                high_low,
                high_close,
                low_close,
            ],
            axis=1,
        ).max(axis=1)

        data["ATR"] = (
            tr.rolling(period).mean()
        )

        return data