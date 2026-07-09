import pandas as pd


class EMA:

    @staticmethod
    def calculate(df: pd.DataFrame, period: int):

        column = f"EMA_{period}"

        df[column] = (
            df["close"]
            .ewm(span=period, adjust=False)
            .mean()
        )

        return df