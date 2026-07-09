from config.settings import weights


class AIScorer:

    def score(self, df):

        score = 0

        last = df.iloc[-1]

        # EMA Alignment
        if last["EMA20"] > last["EMA50"] > last["EMA200"]:
            score += weights.get("ema_alignment")

        # RSI
        if 50 < last["RSI"] < 70:
            score += weights.get("rsi")

        # MACD
        if last["MACD"] > last["MACD_SIGNAL"]:
            score += weights.get("macd")

        return score