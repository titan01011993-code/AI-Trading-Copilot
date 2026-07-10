from core.market_state import MarketState
from core.decision_state import DecisionState


class DecisionEngine:
    """
    AI Decision Engine V3

    Score Distribution
    ------------------
    Trend           : 30
    Momentum        : 25
    Structure       : 20
    Institutional   : 25

    Total           : 100
    """

    WEIGHTS = {

        "TREND": 15,
        "SUPERTREND": 10,
        "ADX": 5,

        "RSI": 10,
        "MACD": 15,

        "BOS": 10,
        "CHOCH": 10,

        "VWAP": 10,
        "ORDER_BLOCK": 5,
        "FVG": 5,
        "LIQUIDITY": 5,

    }

    @classmethod
    def analyze(cls, state: MarketState) -> DecisionState:

        buy = 0
        sell = 0

        reasons = []

        w = cls.WEIGHTS

        # =====================================================
        # TREND
        # =====================================================

        if state.trend.direction == "Bullish":

            buy += w["TREND"]
            reasons.append("Bullish Trend")

        elif state.trend.direction == "Bearish":

            sell += w["TREND"]
            reasons.append("Bearish Trend")

        # -----------------------------------------------------

        if state.trend.supertrend == "Bullish":

            buy += w["SUPERTREND"]
            reasons.append("Bullish SuperTrend")

        elif state.trend.supertrend == "Bearish":

            sell += w["SUPERTREND"]
            reasons.append("Bearish SuperTrend")

        # -----------------------------------------------------

        if state.trend.adx >= 25:

            if state.trend.direction == "Bullish":

                buy += w["ADX"]
                reasons.append("Strong Bull Trend")

            elif state.trend.direction == "Bearish":

                sell += w["ADX"]
                reasons.append("Strong Bear Trend")

        # =====================================================
        # MOMENTUM
        # =====================================================

        if state.momentum.rsi >= 60:

            buy += w["RSI"]
            reasons.append("Strong RSI")

        elif state.momentum.rsi <= 40:

            sell += w["RSI"]
            reasons.append("Weak RSI")

        # -----------------------------------------------------

        if state.momentum.macd > state.momentum.macd_signal:

            buy += w["MACD"]
            reasons.append("Bullish MACD")

        else:

            sell += w["MACD"]
            reasons.append("Bearish MACD")

        # =====================================================
        # STRUCTURE
        # =====================================================

        if state.structure.bos == "Bullish":

            buy += w["BOS"]
            reasons.append("Bullish BOS")

        elif state.structure.bos == "Bearish":

            sell += w["BOS"]
            reasons.append("Bearish BOS")

        # -----------------------------------------------------

        if state.structure.choch == "Bullish":

            buy += w["CHOCH"]
            reasons.append("Bullish CHOCH")

        elif state.structure.choch == "Bearish":

            sell += w["CHOCH"]
            reasons.append("Bearish CHOCH")

        # =====================================================
        # INSTITUTIONAL
        # =====================================================

        if state.volume.vwap_signal == "Bullish":

            buy += w["VWAP"]
            reasons.append("Above VWAP")

        elif state.volume.vwap_signal == "Bearish":

            sell += w["VWAP"]
            reasons.append("Below VWAP")

        # -----------------------------------------------------
        # ORDER BLOCK
        # -----------------------------------------------------

        if len(state.smart_money.bullish_order_blocks) > 0:

            buy += w["ORDER_BLOCK"]
            reasons.append("Bullish Order Block")

        if len(state.smart_money.bearish_order_blocks) > 0:

            sell += w["ORDER_BLOCK"]
            reasons.append("Bearish Order Block")

        # -----------------------------------------------------
        # FAIR VALUE GAP
        # -----------------------------------------------------

        if len(state.smart_money.bullish_fvgs) > 0:

            buy += w["FVG"]
            reasons.append("Bullish FVG")

        if len(state.smart_money.bearish_fvgs) > 0:

            sell += w["FVG"]
            reasons.append("Bearish FVG")

        # -----------------------------------------------------
        # LIQUIDITY
        # -----------------------------------------------------

        if len(state.smart_money.buy_side_liquidity) > 0:

            buy += w["LIQUIDITY"]
            reasons.append("Buy Side Liquidity")

        if len(state.smart_money.sell_side_liquidity) > 0:

            sell += w["LIQUIDITY"]
            reasons.append("Sell Side Liquidity")

        # =====================================================
        # FINAL SCORE
        # =====================================================

        buy = min(buy, 100)
        sell = min(sell, 100)

        hold = max(0, 100 - max(buy, sell))

        # =====================================================
        # MARKET BIAS
        # =====================================================

        if buy >= 80:

            bias = "STRONG BUY"

        elif buy >= 60:

            bias = "BUY"

        elif sell >= 80:

            bias = "STRONG SELL"

        elif sell >= 60:

            bias = "SELL"

        else:

            bias = "WAIT"

        confidence = max(buy, sell)

        return DecisionState(

            buy_score=buy,

            sell_score=sell,

            hold_score=hold,

            bias=bias,

            confidence=confidence,

            reasons=reasons,

        )