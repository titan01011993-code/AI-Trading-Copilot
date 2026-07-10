from core.market_state import MarketState
from core.trade_signal import TradeSignal


class SignalEngine:

    @staticmethod
    def generate(state: MarketState) -> TradeSignal:

        score = state.score.technical_score

        trend = state.trend.direction

        supertrend = state.trend.supertrend

        vwap = state.volume.vwap

        bos = state.structure.bos

        choch = state.structure.choch

        support = state.structure.support

        resistance = state.structure.resistance

        atr = max(state.trend.adx, 1)

        close = state.price.close

        reasons = []

        # ======================================================
        # BUY
        # ======================================================

        if (

            score >= 70

            and trend == "Bullish"

            and supertrend == "Bullish"

            and vwap == "Bullish"

        ):

            stoploss = support if support else close - (2 * atr)

            risk = close - stoploss

            return TradeSignal(

                signal="BUY",

                entry=round(close, 2),

                stoploss=round(stoploss, 2),

                target1=round(close + risk * 2, 2),

                target2=round(close + risk * 3, 2),

                target3=round(close + risk * 4, 2),

                risk=round(risk, 2),

                reward=round(risk * 2, 2),

                risk_reward="1 : 2",

                reasons=[

                    "Bullish Trend",

                    "Bullish SuperTrend",

                    "Above VWAP",

                    "Technical Score >=70",

                ]

            )

        # ======================================================
        # SELL
        # ======================================================

        if (

            score <= 30

            and trend == "Bearish"

            and supertrend == "Bearish"

            and vwap == "Bearish"

        ):

            stoploss = resistance if resistance else close + (2 * atr)

            risk = stoploss - close

            return TradeSignal(

                signal="SELL",

                entry=round(close, 2),

                stoploss=round(stoploss, 2),

                target1=round(close - risk * 2, 2),

                target2=round(close - risk * 3, 2),

                target3=round(close - risk * 4, 2),

                risk=round(risk, 2),

                reward=round(risk * 2, 2),

                risk_reward="1 : 2",

                reasons=[

                    "Bearish Trend",

                    "Bearish SuperTrend",

                    "Below VWAP",

                    "Technical Score <=30",

                ]

            )

        # ======================================================
        # WAIT
        # ======================================================

        if bos:

            reasons.append(f"BOS : {bos}")

        if choch:

            reasons.append(f"CHOCH : {choch}")

        return TradeSignal(

            signal="WAIT",

            entry=None,

            stoploss=None,

            target1=None,

            target2=None,

            target3=None,

            risk=None,

            reward=None,

            risk_reward=None,

            reasons=reasons,

        )