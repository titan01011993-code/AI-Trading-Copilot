from core.alignment import Alignment


class MultiTimeframeEngine:

    @staticmethod
    def analyze(states: dict):

        bullish = 0
        bearish = 0
        neutral = 0

        for tf, state in states.items():

            bias = state.decision.bias

            if bias in ("BUY", "STRONG BUY"):
                bullish += 1
            elif bias in ("SELL", "STRONG SELL"):
                bearish += 1
            else:
                neutral += 1

        total = bullish + bearish + neutral
        if total == 0:
            total = 1

        alignment = round(max(bullish, bearish) / total * 100, 2)

        if bullish > bearish:
            direction = "Bullish"
        elif bearish > bullish:
            direction = "Bearish"
        else:
            direction = "Neutral"

        return Alignment(
            bullish=bullish,
            bearish=bearish,
            neutral=neutral,
            alignment_score=alignment,
            direction=direction,
        )