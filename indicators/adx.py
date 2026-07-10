import numpy as np
import pandas as pd


class ADXIndicator:
    """
    Average Directional Index (ADX)

    Output:
        PLUS_DI
        MINUS_DI
        DX
        ADX
        ADX_SIGNAL
        TREND_STRENGTH
    """

    @staticmethod
    def calculate(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:

        data = df.copy()

        # --------------------------
        # True Range
        # --------------------------

        high = data["high"]
        low = data["low"]
        close = data["close"]

        prev_close = close.shift(1)

        tr1 = high - low
        tr2 = (high - prev_close).abs()
        tr3 = (low - prev_close).abs()

        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        atr = tr.ewm(alpha=1 / period, adjust=False).mean()

        # --------------------------
        # Directional Movement
        # --------------------------

        up_move = high.diff()
        down_move = -low.diff()

        plus_dm = np.where(
            (up_move > down_move) & (up_move > 0),
            up_move,
            0,
        )

        minus_dm = np.where(
            (down_move > up_move) & (down_move > 0),
            down_move,
            0,
        )

        plus_dm = pd.Series(plus_dm, index=data.index)
        minus_dm = pd.Series(minus_dm, index=data.index)

        plus_dm = plus_dm.ewm(alpha=1 / period, adjust=False).mean()
        minus_dm = minus_dm.ewm(alpha=1 / period, adjust=False).mean()

        # --------------------------
        # DI
        # --------------------------

        plus_di = 100 * (plus_dm / atr)
        minus_di = 100 * (minus_dm / atr)

        # --------------------------
        # DX
        # --------------------------

        dx = (
            (plus_di - minus_di).abs()
            / (plus_di + minus_di)
        ) * 100

        adx = dx.ewm(alpha=1 / period, adjust=False).mean()

        data["PLUS_DI"] = plus_di
        data["MINUS_DI"] = minus_di
        data["DX"] = dx
        data["ADX"] = adx

        # --------------------------
        # ADX Signal
        # --------------------------

        data["ADX_SIGNAL"] = "Sideways"

        bullish = (
            (data["PLUS_DI"] > data["MINUS_DI"])
            & (data["ADX"] >= 25)
        )

        bearish = (
            (data["MINUS_DI"] > data["PLUS_DI"])
            & (data["ADX"] >= 25)
        )

        data.loc[bullish, "ADX_SIGNAL"] = "Bullish"
        data.loc[bearish, "ADX_SIGNAL"] = "Bearish"

        # --------------------------
        # Trend Strength
        # --------------------------

        data["TREND_STRENGTH"] = "Weak"

        data.loc[
            data["ADX"] >= 20,
            "TREND_STRENGTH"
        ] = "Building"

        data.loc[
            data["ADX"] >= 25,
            "TREND_STRENGTH"
        ] = "Strong"

        data.loc[
            data["ADX"] >= 40,
            "TREND_STRENGTH"
        ] = "Very Strong"

        data.loc[
            data["ADX"] >= 60,
            "TREND_STRENGTH"
        ] = "Extreme"

        return data