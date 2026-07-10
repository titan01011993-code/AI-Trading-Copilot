from indicators.ema import EMAIndicator
from indicators.rsi import RSIIndicator
from indicators.macd import MACDIndicator
from indicators.atr import ATRIndicator
from indicators.adx import ADXIndicator
from indicators.supertrend import SuperTrendIndicator
from indicators.volume import VolumeIndicator
from indicators.vwap import VWAPIndicator

class IndicatorPipeline:

    @staticmethod
    def calculate(df):

        # =========================
        # Trend Indicators
        # =========================

        df = EMAIndicator.calculate(df)

        # =========================
        # Momentum Indicators
        # =========================

        df = RSIIndicator.calculate(df)
        df = MACDIndicator.calculate(df)
        df = ADXIndicator.calculate(df)

        # =========================
        # Volatility Indicators
        # =========================

        df = ATRIndicator.calculate(df)

        
        #=========================
        # Supertrend Indicator
        #=========================
        df = SuperTrendIndicator.calculate(df)

        
        # ========================
        # Volume Indicators
        # =========================

        df = VolumeIndicator.calculate(df)

        #========================
        # VWAP Indicator
        # =========================
        
        df = VWAPIndicator.calculate(df)

        return df