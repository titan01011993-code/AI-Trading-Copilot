import pandas as pd


class MACDIndicator:

    @staticmethod
    def calculate(
        df: pd.DataFrame,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9,
    ) -> pd.DataFrame:

        data = df.copy()

        ema_fast = data["close"].ewm(span=fast, adjust=False).mean()
        ema_slow = data["close"].ewm(span=slow, adjust=False).mean()

        data["MACD"] = ema_fast - ema_slow
        data["MACD_SIGNAL"] = (
            data["MACD"]
            .ewm(span=signal, adjust=False)
            .mean()
        )

        data["MACD_HIST"] = (
            data["MACD"] - data["MACD_SIGNAL"]
        )

        return data