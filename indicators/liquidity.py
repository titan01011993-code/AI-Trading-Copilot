import numpy as np


class LiquidityIndicator:

    @staticmethod
    def calculate(df, tolerance=0.0015):
        """
        tolerance = 0.15%
        """

        df = df.copy()

        df["EQUAL_HIGH"] = False
        df["EQUAL_LOW"] = False

        df["BUY_SIDE_LIQUIDITY"] = np.nan
        df["SELL_SIDE_LIQUIDITY"] = np.nan

        swing_highs = []
        swing_lows = []

        for i in range(len(df)):

            # ---------- Equal High ----------
            if df.at[df.index[i], "SWING_HIGH"]:

                current_high = df.at[df.index[i], "high"]

                for prev in swing_highs:

                    if abs(current_high - prev) / prev <= tolerance:

                        df.at[df.index[i], "EQUAL_HIGH"] = True
                        df.at[df.index[i], "BUY_SIDE_LIQUIDITY"] = current_high
                        break

                swing_highs.append(current_high)

            # ---------- Equal Low ----------
            if df.at[df.index[i], "SWING_LOW"]:

                current_low = df.at[df.index[i], "low"]

                for prev in swing_lows:

                    if abs(current_low - prev) / prev <= tolerance:

                        df.at[df.index[i], "EQUAL_LOW"] = True
                        df.at[df.index[i], "SELL_SIDE_LIQUIDITY"] = current_low
                        break

                swing_lows.append(current_low)

        return df