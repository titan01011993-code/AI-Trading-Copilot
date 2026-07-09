import pandas as pd


class ScoringEngine:

    @staticmethod
    def technical_score(df: pd.DataFrame):

        last = df.iloc[-1]

        score = 50          # Neutral starting score
        reasons = []

        # EMA
        if last["EMA_20"] > last["EMA_50"]:
            score += 10
            reasons.append("EMA20 > EMA50")
        else:
            score -= 10
            reasons.append("EMA20 < EMA50")

        if last["EMA_50"] > last["EMA_200"]:
            score += 15
            reasons.append("EMA50 > EMA200")
        else:
            score -= 15
            reasons.append("EMA50 < EMA200")

        # RSI
        if last["RSI"] < 30:
            score += 15
            reasons.append("RSI Oversold")

        elif last["RSI"] > 70:
            score -= 15
            reasons.append("RSI Overbought")

        else:
            reasons.append("RSI Neutral")

        # MACD
        if last["MACD"] > last["MACD_SIGNAL"]:
            score += 20
            reasons.append("MACD Bullish")
        else:
            score -= 20
            reasons.append("MACD Bearish")

        # Volume
        avg_vol = df["volume"].tail(20).mean()

        if last["volume"] > avg_vol:
            score += 10
            reasons.append("High Volume")
        else:
            score -= 10
            reasons.append("Low Volume")

        score = max(0, min(score, 100))

        return score, reasons