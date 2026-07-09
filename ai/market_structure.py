import pandas as pd


class MarketStructure:

    @staticmethod
    def analyze(df: pd.DataFrame):

        highs = df["high"].tail(5).tolist()
        lows = df["low"].tail(5).tolist()

        higher_high = highs[-1] > highs[-2]
        higher_low = lows[-1] > lows[-2]

        lower_high = highs[-1] < highs[-2]
        lower_low = lows[-1] < lows[-2]

        if higher_high and higher_low:
            trend = "UPTREND"

        elif lower_high and lower_low:
            trend = "DOWNTREND"

        else:
            trend = "SIDEWAYS"

        return {
            "trend": trend,
            "higher_high": higher_high,
            "higher_low": higher_low,
            "lower_high": lower_high,
            "lower_low": lower_low,
        }