import numpy as np


class BOSIndicator:

    @staticmethod
    def calculate(df):

        df = df.copy()

        df["BOS"] = False
        df["BOS_DIRECTION"] = None

        last_swing_high = np.nan
        last_swing_low = np.nan

        bullish_broken = False
        bearish_broken = False

        for i in range(len(df)):

            # New Swing High
            if df.at[df.index[i], "SWING_HIGH"]:
                last_swing_high = df.at[df.index[i], "high"]
                bullish_broken = False

            # New Swing Low
            if df.at[df.index[i], "SWING_LOW"]:
                last_swing_low = df.at[df.index[i], "low"]
                bearish_broken = False

            close = df.at[df.index[i], "close"]

            # Bullish BOS
            if (
                not np.isnan(last_swing_high)
                and not bullish_broken
                and close > last_swing_high
            ):

                df.at[df.index[i], "BOS"] = True
                df.at[df.index[i], "BOS_DIRECTION"] = "Bullish"

                bullish_broken = True

            # Bearish BOS
            if (
                not np.isnan(last_swing_low)
                and not bearish_broken
                and close < last_swing_low
            ):

                df.at[df.index[i], "BOS"] = True
                df.at[df.index[i], "BOS_DIRECTION"] = "Bearish"

                bearish_broken = True

        return df