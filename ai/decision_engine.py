import pandas as pd


class DecisionEngine:

    @staticmethod
    def analyze(df: pd.DataFrame):

        last = df.iloc[-1]

        score = 0
        reasons = []

        # Trend
        bullish_trend = (
            last["EMA_20"] >
            last["EMA_50"] >
            last["EMA_200"]
        )

        if bullish_trend:
            score += 40
            reasons.append("EMA Trend Bullish")
        else:
            score -= 40
            reasons.append("EMA Trend Bearish")

        # RSI
        if last["RSI"] < 30:
            score += 30
            reasons.append("RSI Oversold")

        elif last["RSI"] > 70:
            score -= 30
            reasons.append("RSI Overbought")

        else:
            reasons.append("RSI Neutral")

        # MACD
        if last["MACD"] > last["MACD_SIGNAL"]:
            score += 30
            reasons.append("MACD Bullish")

        else:
            score -= 30
            reasons.append("MACD Bearish")

        # Final Signal
        if score >= 40:
            signal = "BUY"

        elif score <= -40:
            signal = "SELL"

        else:
            signal = "HOLD"

        confidence = min(abs(score), 100)

        entry = round(last["close"], 2)

        atr = round(last["ATR"], 2)

        if signal == "BUY":

            stop = round(entry - (1.5 * atr), 2)

            target1 = round(entry + (2 * atr), 2)

            target2 = round(entry + (4 * atr), 2)

        elif signal == "SELL":

            stop = round(entry - (1.5 * atr), 2)

            target1 = round(entry + (2 * atr), 2)

            target2 = round(entry + (4 * atr), 2)

        else:

            stop = entry

            target1 = entry

            target2 = entry

        risk = abs(entry - stop)
        reward = abs(target1 - entry)

        rr = round(reward / risk, 2) if risk else 0

        return {

            "signal": signal,

            "confidence": confidence,

            "entry": entry,

            "stop": stop,

            "target1": target1,

            "target2": target2,

            "rr": rr,

            "reasons": reasons,
        }