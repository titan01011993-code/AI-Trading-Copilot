class MomentumFeatures:

    @staticmethod
    def calculate(df):

        data = df.copy()

        data["RSI_STRENGTH"] = (

            data["RSI"] - 50

        ) / 50

        data["MACD_DISTANCE"] = (

            data["MACD"]

            -

            data["MACD_SIGNAL"]

        )

        data["MACD_BULLISH"] = (

            data["MACD"]

            >

            data["MACD_SIGNAL"]

        ).astype(int)

        return data