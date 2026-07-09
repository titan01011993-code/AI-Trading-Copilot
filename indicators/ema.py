import pandas as pd


class EMAIndicator:
    """
    Exponential Moving Average Indicator
    """

    @staticmethod
    def calculate(
        df: pd.DataFrame,
        periods=(20, 50, 200),
    ) -> pd.DataFrame:

        data = df.copy()

        for period in periods:

            data[f"EMA_{period}"] = (
                data["close"]
                .ewm(span=period, adjust=False)
                .mean()
            )

        return data