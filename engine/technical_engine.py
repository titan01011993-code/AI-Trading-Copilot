import pandas as pd

from core.market_state import (
    MarketState,
    PriceState,
    TrendState,
    MomentumState,
    VolatilityState,
    VolumeState,
    StructureState,
    SmartMoneyState,
    ScoreState,
)


class TechnicalEngine:
    """
    Technical Engine

    Converts the latest dataframe row into a
    normalized MarketState object.
    """

    @staticmethod
    def _safe_float(value):

        if pd.isna(value):
            return None

        return float(value)

    @classmethod
    def analyze(cls, symbol: str, df) -> MarketState:

        latest = df.iloc[-1]

        # =====================================================
        # PRICE
        # =====================================================

        price = PriceState(

            symbol=symbol,

            datetime=str(latest["datetime"]),

            open=float(latest["open"]),

            high=float(latest["high"]),

            low=float(latest["low"]),

            close=float(latest["close"]),

            volume=float(latest["volume"]),

        )

        # =====================================================
        # TREND
        # =====================================================

        trend = TrendState(

            ema20=float(latest["EMA_20"]),

            ema50=float(latest["EMA_50"]),

            ema200=float(latest["EMA_200"]),

            supertrend=str(latest["SUPERTREND_DIRECTION"]),

            adx=float(latest["ADX"]),

            direction=str(latest["TECHNICAL_BIAS"]),

            strength=str(latest["SIGNAL_STRENGTH"]),

        )

        # =====================================================
        # MOMENTUM
        # =====================================================

        momentum = MomentumState(

            rsi=float(latest["RSI"]),

            macd=float(latest["MACD"]),

            macd_signal=float(latest["MACD_SIGNAL"]),

            macd_hist=float(latest["MACD_HIST"]),

        )

        # =====================================================
        # VOLATILITY
        # =====================================================

        volatility = VolatilityState(

            atr=float(latest["ATR"]),

            atr_signal=latest.get("ADX_SIGNAL"),

        )

        # =====================================================
        # VOLUME
        # =====================================================

        volume = VolumeState(

            vwap_signal=str(latest["VWAP_SIGNAL"]),

            volume_signal=latest.get("VOLUME_COLOR"),

        )

        # =====================================================
        # STRUCTURE
        # =====================================================

        supports = []

        resistances = []

        value = cls._safe_float(latest.get("SUPPORT"))

        if value is not None:
            supports.append(value)

        value = cls._safe_float(latest.get("RESISTANCE"))

        if value is not None:
            resistances.append(value)

        structure = StructureState(

            bos=latest.get("BOS_DIRECTION"),

            choch=latest.get("CHOCH_DIRECTION"),

            supports=supports,

            resistances=resistances,

        )

        # =====================================================
        # SMART MONEY
        # =====================================================

        bullish_ob = []

        bearish_ob = []

        bullish_fvg = []

        bearish_fvg = []

        buy_liquidity = []

        sell_liquidity = []

        liquidity_sweeps = []

        mitigated_blocks = []

        # -------------------------
        # ORDER BLOCK
        # -------------------------

        if bool(latest.get("OB_VALID", False)):

            if latest.get("OB_TYPE") == "Bullish":

                value = cls._safe_float(latest.get("OB_LOW"))

                if value is not None:
                    bullish_ob.append(value)

            elif latest.get("OB_TYPE") == "Bearish":

                value = cls._safe_float(latest.get("OB_HIGH"))

                if value is not None:
                    bearish_ob.append(value)

        # -------------------------
        # FVG
        # -------------------------

        if bool(latest.get("FVG_VALID", False)):

            if latest.get("FVG_TYPE") == "Bullish":

                value = cls._safe_float(latest.get("FVG_BOTTOM"))

                if value is not None:
                    bullish_fvg.append(value)

            elif latest.get("FVG_TYPE") == "Bearish":

                value = cls._safe_float(latest.get("FVG_TOP"))

                if value is not None:
                    bearish_fvg.append(value)

        # -------------------------
        # BUY SIDE LIQUIDITY
        # -------------------------

        value = cls._safe_float(

            latest.get("BUY_SIDE_LIQUIDITY")

        )

        if value is not None:

            buy_liquidity.append(value)

        # -------------------------
        # SELL SIDE LIQUIDITY
        # -------------------------

        value = cls._safe_float(

            latest.get("SELL_SIDE_LIQUIDITY")

        )

        if value is not None:

            sell_liquidity.append(value)

        # -------------------------
        # SWEEP
        # -------------------------

        if bool(latest.get("SWEEP", False)):

            value = cls._safe_float(

                latest.get("SWEEP_LEVEL")

            )

            if value is not None:

                liquidity_sweeps.append(value)

        # -------------------------
        # MITIGATION
        # -------------------------

        if bool(latest.get("MITIGATED", False)):

            value = cls._safe_float(

                latest.get("MITIGATION_PRICE")

            )

            if value is not None:

                mitigated_blocks.append(value)

        smart_money = SmartMoneyState(

            bullish_order_blocks=bullish_ob,

            bearish_order_blocks=bearish_ob,

            bullish_fvgs=bullish_fvg,

            bearish_fvgs=bearish_fvg,

            buy_side_liquidity=buy_liquidity,

            sell_side_liquidity=sell_liquidity,

            liquidity_sweeps=liquidity_sweeps,

            mitigated_blocks=mitigated_blocks,

        )

        # =====================================================
        # SCORE
        # =====================================================

        score = ScoreState(

            trend_score=int(latest["TREND_SCORE"]),

            momentum_score=int(latest["MOMENTUM_SCORE"]),

            volume_score=int(latest["VOLUME_SCORE"]),

            volatility_score=int(latest["VOLATILITY_SCORE"]),

            structure_score=int(latest["STRUCTURE_SCORE"]),

            technical_score=int(latest["TECHNICAL_SCORE"]),

            confidence=str(latest["CONFIDENCE"]),

        )

        # =====================================================
        # FINAL MARKET STATE
        # =====================================================

        return MarketState(

            price=price,

            trend=trend,

            momentum=momentum,

            volatility=volatility,

            volume=volume,

            structure=structure,

            smart_money=smart_money,

            score=score,

        )