import numpy as np


class LiquiditySweepIndicator:

    @staticmethod
    def calculate(df):

        df = df.copy()

        df["SWEEP"] = False
        df["SWEEP_DIRECTION"] = None
        df["SWEEP_LEVEL"] = np.nan
        df["SWEEP_INDEX"] = np.nan

        last_buy_liquidity = np.nan
        last_sell_liquidity = np.nan

        for i in range(len(df)):

            # --------------------------
            # Update latest liquidity
            # --------------------------

            if df.at[df.index[i], "EQUAL_HIGH"]:

                last_buy_liquidity = df.at[df.index[i], "BUY_SIDE_LIQUIDITY"]

            if df.at[df.index[i], "EQUAL_LOW"]:

                last_sell_liquidity = df.at[df.index[i], "SELL_SIDE_LIQUIDITY"]

            high = df.at[df.index[i], "high"]
            low = df.at[df.index[i], "low"]
            close = df.at[df.index[i], "close"]

            # --------------------------
            # Buy Side Sweep
            # --------------------------

            if not np.isnan(last_buy_liquidity):

                if high > last_buy_liquidity and close < last_buy_liquidity:

                    df.at[df.index[i], "SWEEP"] = True
                    df.at[df.index[i], "SWEEP_DIRECTION"] = "BUY_SIDE"
                    df.at[df.index[i], "SWEEP_LEVEL"] = last_buy_liquidity
                    df.at[df.index[i], "SWEEP_INDEX"] = i

                    last_buy_liquidity = np.nan

            # --------------------------
            # Sell Side Sweep
            # --------------------------

            if not np.isnan(last_sell_liquidity):

                if low < last_sell_liquidity and close > last_sell_liquidity:

                    df.at[df.index[i], "SWEEP"] = True
                    df.at[df.index[i], "SWEEP_DIRECTION"] = "SELL_SIDE"
                    df.at[df.index[i], "SWEEP_LEVEL"] = last_sell_liquidity
                    df.at[df.index[i], "SWEEP_INDEX"] = i

                    last_sell_liquidity = np.nan

        return df