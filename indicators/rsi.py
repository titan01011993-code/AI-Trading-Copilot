import pandas as pd


class RSIIndicator:
    """
    Relative Strength Index (RSI)
    """

    @staticmethod
    def calculate(
        df: pd.DataFrame,
        period: int = 14,
    ) -> pd.DataFrame:

        data = df.copy()

        delta = data["close"].diff()

        gain = delta.clip(lower=0)

        loss = -delta.clip(upper=0)

        avg_gain = gain.ewm(
            alpha=1 / period,
            adjust=False
        ).mean()

        avg_loss = loss.ewm(
            alpha=1 / period,
            adjust=False
        ).mean()

        rs = avg_gain / avg_loss

        data["RSI"] = 100 - (100 / (1 + rs))

        return data