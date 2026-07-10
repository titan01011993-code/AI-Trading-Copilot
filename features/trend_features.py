import numpy as np


class TrendFeatures:

    @staticmethod
    def calculate(df):

        data = df.copy()

        data["EMA_ALIGNMENT"] = (
            (
                (data["EMA_20"] > data["EMA_50"])
                &
                (data["EMA_50"] > data["EMA_200"])
            )
        ).astype(int)

        data["EMA_DISTANCE"] = (
            (
                data["EMA_20"] -
                data["EMA_200"]
            )
            /
            data["EMA_200"]
        ) * 100

        data["PRICE_ABOVE_EMA20"] = (
            data["close"] >
            data["EMA_20"]
        ).astype(int)

        return data