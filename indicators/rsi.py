import pandas as pd
import ta


class RSI:

    @staticmethod
    def calculate(df, period=14):

        df["RSI"] = ta.momentum.RSIIndicator(
            close=df["close"],
            window=period,
        ).rsi()

        return df