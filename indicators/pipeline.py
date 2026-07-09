from indicators.ema import EMA
from indicators.rsi import RSI
from indicators.macd import MACD


class IndicatorPipeline:

    @staticmethod
    def run(df):

        df = EMA.calculate(df, 20)
        df = EMA.calculate(df, 50)
        df = EMA.calculate(df, 200)

        df = RSI.calculate(df)

        df = MACD.calculate(df)

        return df