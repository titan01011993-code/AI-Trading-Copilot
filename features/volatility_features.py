class VolatilityFeatures:

    @staticmethod
    def calculate(df):

        data = df.copy()

        data["ATR_PERCENT"] = (

            data["ATR"]

            /

            data["close"]

        ) * 100

        return data