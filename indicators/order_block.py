import numpy as np


class OrderBlockIndicator:

    @staticmethod
    def calculate(df):

        df = df.copy()

        cols = [
            "OB_TYPE",
            "OB_HIGH",
            "OB_LOW",
            "OB_OPEN",
            "OB_CLOSE",
            "OB_INDEX",
            "OB_MITIGATED",
            "OB_VALID",
        ]

        for col in cols:
            df[col] = np.nan

        df["OB_TYPE"] = None
        df["OB_MITIGATED"] = False
        df["OB_VALID"] = False

        for i in range(1, len(df)):

            if not df.at[df.index[i], "BOS"]:
                continue

            direction = df.at[df.index[i], "BOS_DIRECTION"]

            # Bullish Order Block
            if direction == "Bullish":

                for j in range(i - 1, -1, -1):

                    if df.at[df.index[j], "close"] < df.at[df.index[j], "open"]:

                        df.at[df.index[i], "OB_TYPE"] = "Bullish"
                        df.at[df.index[i], "OB_HIGH"] = df.at[df.index[j], "high"]
                        df.at[df.index[i], "OB_LOW"] = df.at[df.index[j], "low"]
                        df.at[df.index[i], "OB_OPEN"] = df.at[df.index[j], "open"]
                        df.at[df.index[i], "OB_CLOSE"] = df.at[df.index[j], "close"]
                        df.at[df.index[i], "OB_INDEX"] = j
                        df.at[df.index[i], "OB_VALID"] = True
                        break

            # Bearish Order Block
            if direction == "Bearish":

                for j in range(i - 1, -1, -1):

                    if df.at[df.index[j], "close"] > df.at[df.index[j], "open"]:

                        df.at[df.index[i], "OB_TYPE"] = "Bearish"
                        df.at[df.index[i], "OB_HIGH"] = df.at[df.index[j], "high"]
                        df.at[df.index[i], "OB_LOW"] = df.at[df.index[j], "low"]
                        df.at[df.index[i], "OB_OPEN"] = df.at[df.index[j], "open"]
                        df.at[df.index[i], "OB_CLOSE"] = df.at[df.index[j], "close"]
                        df.at[df.index[i], "OB_INDEX"] = j
                        df.at[df.index[i], "OB_VALID"] = True
                        break

        return df