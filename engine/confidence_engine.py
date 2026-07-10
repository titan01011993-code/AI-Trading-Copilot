from core.market_state import MarketState
from core.decision_state import DecisionState


class ConfidenceEngine:

    @staticmethod
    def calculate(
        state: MarketState,
        decision: DecisionState,
    ) -> float:

        score = 0

        total = 0

        # ===========================================
        # TREND
        # ===========================================

        total += 1

        if state.trend.direction != "Neutral":
            score += 1

        total += 1

        if state.trend.supertrend == state.trend.direction:
            score += 1

        total += 1

        if state.trend.adx >= 25:
            score += 1

        # ===========================================
        # MOMENTUM
        # ===========================================

        total += 1

        if (
            decision.bias.startswith("BUY")
            and state.momentum.rsi >= 55
        ) or (
            decision.bias.startswith("SELL")
            and state.momentum.rsi <= 45
        ):
            score += 1

        total += 1

        if (
            decision.bias.startswith("BUY")
            and state.momentum.macd > state.momentum.macd_signal
        ) or (
            decision.bias.startswith("SELL")
            and state.momentum.macd < state.momentum.macd_signal
        ):
            score += 1

        # ===========================================
        # STRUCTURE
        # ===========================================

        total += 1

        if state.structure.bos is not None:
            score += 1

        total += 1

        if state.structure.choch is not None:
            score += 1

        # ===========================================
        # INSTITUTIONAL
        # ===========================================

        total += 1

        if state.smart_money.bullish_order_blocks or state.smart_money.bearish_order_blocks:
            score += 1

        total += 1

        if state.smart_money.bullish_fvgs or state.smart_money.bearish_fvgs:
            score += 1

        total += 1

        if (
            state.smart_money.buy_side_liquidity
            or state.smart_money.sell_side_liquidity
        ):
            score += 1

        confidence = round(score / total * 100, 2)

        return confidence