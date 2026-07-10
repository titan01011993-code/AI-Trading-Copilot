import numpy as np


class SwingIndicator:

    @staticmethod
    def calculate(df, lookback=2):

        df = df.copy()

        df["SWING_HIGH"] = False
        df["SWING_LOW"] = False

        df["SWING_HIGH_PRICE"] = np.nan
        df["SWING_LOW_PRICE"] = np.nan

        highs = df["high"].values
        lows = df["low"].values

        for i in range(lookback, len(df) - lookback):

            high = highs[i]
            low = lows[i]

            # Swing High
            if all(high > highs[i - j] for j in range(1, lookback + 1)) and \
               all(high > highs[i + j] for j in range(1, lookback + 1)):

                df.at[df.index[i], "SWING_HIGH"] = True
                df.at[df.index[i], "SWING_HIGH_PRICE"] = high

            # Swing Low
            if all(low < lows[i - j] for j in range(1, lookback + 1)) and \
               all(low < lows[i + j] for j in range(1, lookback + 1)):

                df.at[df.index[i], "SWING_LOW"] = True
                df.at[df.index[i], "SWING_LOW_PRICE"] = low

        return df