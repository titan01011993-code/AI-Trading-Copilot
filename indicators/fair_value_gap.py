import numpy as np


class FairValueGapIndicator:

    @staticmethod
    def calculate(df):

        df = df.copy()

        cols = [
            "FVG_TYPE",
            "FVG_TOP",
            "FVG_BOTTOM",
            "FVG_INDEX",
            "FVG_FILLED",
            "FVG_VALID",
        ]

        for col in cols:
            df[col] = np.nan

        df["FVG_TYPE"] = None
        df["FVG_FILLED"] = False
        df["FVG_VALID"] = False

        for i in range(2, len(df)):

            high1 = df.at[df.index[i - 2], "high"]
            low1 = df.at[df.index[i - 2], "low"]

            high3 = df.at[df.index[i], "high"]
            low3 = df.at[df.index[i], "low"]

            # -----------------------
            # Bullish Fair Value Gap
            # -----------------------

            if low3 > high1:

                df.at[df.index[i], "FVG_TYPE"] = "Bullish"
                df.at[df.index[i], "FVG_TOP"] = low3
                df.at[df.index[i], "FVG_BOTTOM"] = high1
                df.at[df.index[i], "FVG_INDEX"] = i
                df.at[df.index[i], "FVG_VALID"] = True

            # -----------------------
            # Bearish Fair Value Gap
            # -----------------------

            elif high3 < low1:

                df.at[df.index[i], "FVG_TYPE"] = "Bearish"
                df.at[df.index[i], "FVG_TOP"] = low1
                df.at[df.index[i], "FVG_BOTTOM"] = high3
                df.at[df.index[i], "FVG_INDEX"] = i
                df.at[df.index[i], "FVG_VALID"] = True

        return df