import numpy as np


class MitigationIndicator:

    @staticmethod
    def calculate(df):

        df = df.copy()

        df["MITIGATED"] = False
        df["MITIGATION_INDEX"] = np.nan
        df["MITIGATION_PRICE"] = np.nan

        active_obs = []

        for i in range(len(df)):

            # ------------------------
            # Register New Order Block
            # ------------------------

            if df.at[df.index[i], "OB_VALID"]:

                active_obs.append({
                    "type": df.at[df.index[i], "OB_TYPE"],
                    "high": df.at[df.index[i], "OB_HIGH"],
                    "low": df.at[df.index[i], "OB_LOW"],
                    "mitigated": False
                })

            candle_high = df.at[df.index[i], "high"]
            candle_low = df.at[df.index[i], "low"]

            # ------------------------
            # Check Mitigation
            # ------------------------

            for ob in active_obs:

                if ob["mitigated"]:
                    continue

                if candle_low <= ob["high"] and candle_high >= ob["low"]:

                    df.at[df.index[i], "MITIGATED"] = True
                    df.at[df.index[i], "MITIGATION_INDEX"] = i
                    df.at[df.index[i], "MITIGATION_PRICE"] = (
                        ob["high"] + ob["low"]
                    ) / 2

                    ob["mitigated"] = True

        return df