from ai.scorer import AIScorer


class AIAnalyzer:

    def analyze(self, df):

        scorer = AIScorer()

        score = scorer.score(df)

        if score >= 80:
            signal = "STRONG BUY"

        elif score >= 60:
            signal = "BUY"

        elif score >= 40:
            signal = "WAIT"

        else:
            signal = "SELL"

        return {
            "score": score,
            "signal": signal
        }