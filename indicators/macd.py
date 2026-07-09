import ta


class MACD:

    @staticmethod
    def calculate(df):

        macd = ta.trend.MACD(df["close"])

        df["MACD"] = macd.macd()
        df["MACD_SIGNAL"] = macd.macd_signal()
        df["MACD_HIST"] = macd.macd_diff()

        return df