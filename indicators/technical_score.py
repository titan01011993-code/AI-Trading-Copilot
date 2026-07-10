class TechnicalScore:

    @staticmethod
    def calculate(df):

        df = df.copy()

        # =====================================================
        # Initialize
        # =====================================================

        df["TREND_SCORE"] = 0
        df["MOMENTUM_SCORE"] = 0
        df["VOLUME_SCORE"] = 0
        df["VOLATILITY_SCORE"] = 0
        df["STRUCTURE_SCORE"] = 0

        # =====================================================
        # TREND SCORE (30)
        # =====================================================

        if {"EMA_20", "EMA_50", "EMA_200"}.issubset(df.columns):

            df.loc[
                df["EMA_20"] > df["EMA_50"],
                "TREND_SCORE"
            ] += 15

            df.loc[
                df["EMA_50"] > df["EMA_200"],
                "TREND_SCORE"
            ] += 15

        if "SUPERTREND_DIRECTION" in df.columns:

            df.loc[
                df["SUPERTREND_DIRECTION"] == "Bullish",
                "TREND_SCORE"
            ] += 10

        # =====================================================
        # MOMENTUM SCORE (30)
        # =====================================================

        if "RSI" in df.columns:

            df.loc[
                (df["RSI"] >= 55) &
                (df["RSI"] <= 70),
                "MOMENTUM_SCORE"
            ] += 15

        if {"MACD", "MACD_SIGNAL"}.issubset(df.columns):

            df.loc[
                df["MACD"] > df["MACD_SIGNAL"],
                "MOMENTUM_SCORE"
            ] += 15

        if "ADX_SIGNAL" in df.columns:

            df.loc[
                df["ADX_SIGNAL"] == "Bullish",
                "MOMENTUM_SCORE"
            ] += 10

        # =====================================================
        # VOLUME SCORE (20)
        # =====================================================

        if "VOLUME_SIGNAL" in df.columns:

            df.loc[
                df["VOLUME_SIGNAL"] == "Bullish",
                "VOLUME_SCORE"
            ] += 10

        if "VWAP_SIGNAL" in df.columns:

            df.loc[
                df["VWAP_SIGNAL"] == "Bullish",
                "VOLUME_SCORE"
            ] += 10

        # =====================================================
        # VOLATILITY SCORE (10)
        # =====================================================

        if "ATR" in df.columns:

            df.loc[
                df["ATR"] > df["ATR"].shift(1),
                "VOLATILITY_SCORE"
            ] += 10

        # =====================================================
        # STRUCTURE SCORE (40)
        # =====================================================

        if "BOS_DIRECTION" in df.columns:

            df.loc[
                df["BOS_DIRECTION"] == "Bullish",
                "STRUCTURE_SCORE"
            ] += 15

        if "CHOCH_DIRECTION" in df.columns:

            df.loc[
                df["CHOCH_DIRECTION"] == "Bullish",
                "STRUCTURE_SCORE"
            ] += 15

        if {"close", "RESISTANCE"}.issubset(df.columns):

            df.loc[
                df["close"] > df["RESISTANCE"],
                "STRUCTURE_SCORE"
            ] += 10

        # =====================================================
        # FINAL SCORE
        # =====================================================

        df["TECHNICAL_SCORE"] = (

            df["TREND_SCORE"]
            + df["MOMENTUM_SCORE"]
            + df["VOLUME_SCORE"]
            + df["VOLATILITY_SCORE"]
            + df["STRUCTURE_SCORE"]

        )

        # Maximum 100

        df["TECHNICAL_SCORE"] = (
            df["TECHNICAL_SCORE"]
            .clip(lower=0, upper=100)
        )

        # =====================================================
        # MARKET BIAS
        # =====================================================

        df["TECHNICAL_BIAS"] = "Neutral"

        df.loc[
            df["TECHNICAL_SCORE"] >= 70,
            "TECHNICAL_BIAS"
        ] = "Bullish"

        df.loc[
            df["TECHNICAL_SCORE"] <= 30,
            "TECHNICAL_BIAS"
        ] = "Bearish"

        # =====================================================
        # SIGNAL STRENGTH
        # =====================================================

        df["SIGNAL_STRENGTH"] = "Weak"

        df.loc[
            df["TECHNICAL_SCORE"] >= 40,
            "SIGNAL_STRENGTH"
        ] = "Moderate"

        df.loc[
            df["TECHNICAL_SCORE"] >= 70,
            "SIGNAL_STRENGTH"
        ] = "Strong"

        df.loc[
            df["TECHNICAL_SCORE"] >= 90,
            "SIGNAL_STRENGTH"
        ] = "Very Strong"

        # =====================================================
        # DECISION
        # =====================================================

        df["TRADE_DECISION"] = "WAIT"

        df.loc[
            df["TECHNICAL_SCORE"] >= 75,
            "TRADE_DECISION"
        ] = "BUY"

        df.loc[
            df["TECHNICAL_SCORE"] <= 25,
            "TRADE_DECISION"
        ] = "SELL"

        # =====================================================
        # CONFIDENCE
        # =====================================================

        df["CONFIDENCE"] = (
            df["TECHNICAL_SCORE"]
            .astype(int)
            .astype(str)
            + "%"
        )

        return df