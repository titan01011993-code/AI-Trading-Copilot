import numpy as np


class SupportResistanceIndicator:

    @staticmethod
    def calculate(df):

        df = df.copy()

        df["SUPPORT"] = np.nan
        df["RESISTANCE"] = np.nan

        support = np.nan
        resistance = np.nan

        for i in range(len(df)):

            if df.at[df.index[i], "SWING_HIGH"]:
                resistance = df.at[df.index[i], "high"]

            if df.at[df.index[i], "SWING_LOW"]:
                support = df.at[df.index[i], "low"]

            df.at[df.index[i], "SUPPORT"] = support
            df.at[df.index[i], "RESISTANCE"] = resistance

        return df