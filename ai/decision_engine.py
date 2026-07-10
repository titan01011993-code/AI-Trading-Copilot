from typing import Optional
import pandas as pd
from core.models import DecisionOutput
from core.enums import Recommendation, Trend


class DecisionEngine:
    """
    Production-grade decision engine that analyzes technical indicators
    and generates trading signals with entry, exit, and risk metrics.
    
    Requires dataframe with columns: EMA_20, EMA_50, EMA_200, RSI, MACD, MACD_SIGNAL, ATR, close
    """

    # Signal thresholds
    BUY_THRESHOLD = 40
    SELL_THRESHOLD = -40
    
    # ATR multipliers for position sizing
    STOP_LOSS_ATR_MULTIPLE = 1.5
    TARGET1_ATR_MULTIPLE = 2.0
    TARGET2_ATR_MULTIPLE = 4.0

    @staticmethod
    def _validate_dataframe(df: pd.DataFrame) -> None:
        """Validate that dataframe has all required columns."""
        required_columns = [
            "EMA_20", "EMA_50", "EMA_200",
            "RSI", "MACD", "MACD_SIGNAL", "ATR", "close"
        ]
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        if df.empty:
            raise ValueError("DataFrame is empty")

    @staticmethod
    def _analyze_trend(last: pd.Series) -> tuple[str, int, list[str]]:
        """
        Analyze EMA alignment to determine trend.
        
        Returns: (trend_name, score_delta, reasons)
        """
        bullish_trend = (
            last["EMA_20"] > last["EMA_50"] > last["EMA_200"]
        )
        
        if bullish_trend:
            return "BULLISH", 40, ["EMA Alignment Bullish (20 > 50 > 200)"]
        else:
            return "BEARISH", -40, ["EMA Alignment Bearish"]

    @staticmethod
    def _analyze_rsi(last: pd.Series) -> tuple[int, list[str]]:
        """
        Analyze RSI momentum indicator.
        
        Returns: (score_delta, reasons)
        """
        reasons = []
        score = 0
        
        if last["RSI"] < 30:
            score = 30
            reasons.append("RSI Oversold (<30)")
        elif last["RSI"] > 70:
            score = -30
            reasons.append("RSI Overbought (>70)")
        else:
            reasons.append("RSI Neutral")
        
        return score, reasons

    @staticmethod
    def _analyze_macd(last: pd.Series) -> tuple[int, list[str]]:
        """
        Analyze MACD crossover signal.
        
        Returns: (score_delta, reasons)
        """
        if last["MACD"] > last["MACD_SIGNAL"]:
            return 30, ["MACD Bullish (above signal line)"]
        else:
            return -30, ["MACD Bearish (below signal line)"]

    @staticmethod
    def _calculate_levels(
        entry: float,
        atr: float,
        signal: str
    ) -> tuple[float, float, float]:
        """
        Calculate stop loss and target levels based on ATR.
        
        For both BUY and SELL, stop is below entry and targets above.
        This is adjusted in actual trading based on position direction.
        """
        if signal in ("BUY", "SELL"):
            stop_loss = entry - (DecisionEngine.STOP_LOSS_ATR_MULTIPLE * atr)
            target1 = entry + (DecisionEngine.TARGET1_ATR_MULTIPLE * atr)
            target2 = entry + (DecisionEngine.TARGET2_ATR_MULTIPLE * atr)
        else:
            # HOLD: no positions
            stop_loss = entry
            target1 = entry
            target2 = entry
        
        return round(stop_loss, 2), round(target1, 2), round(target2, 2)

    @staticmethod
    def _calculate_risk_reward(
        entry: float,
        stop_loss: float,
        target1: float
    ) -> float:
        """Calculate risk-reward ratio."""
        risk = abs(entry - stop_loss)
        reward = abs(target1 - entry)
        
        if risk == 0:
            return 0.0
        
        return round(reward / risk, 2)

    @staticmethod
    def analyze(
        df: pd.DataFrame,
        symbol: str = "UNKNOWN"
    ) -> DecisionOutput:
        """
        Analyze technical indicators and generate trading decision.
        
        Args:
            df: DataFrame with OHLC and indicators (EMA, RSI, MACD, ATR)
            symbol: Stock symbol for reference
            
        Returns:
            DecisionOutput with signal, confidence, levels, and reasons
            
        Raises:
            ValueError: If dataframe is missing required columns
        """
        DecisionEngine._validate_dataframe(df)
        
        last = df.iloc[-1]
        score = 0
        reasons = []
        
        # Trend analysis
        trend, trend_score, trend_reasons = DecisionEngine._analyze_trend(last)
        score += trend_score
        reasons.extend(trend_reasons)
        
        # RSI analysis
        rsi_score, rsi_reasons = DecisionEngine._analyze_rsi(last)
        score += rsi_score
        reasons.extend(rsi_reasons)
        
        # MACD analysis
        macd_score, macd_reasons = DecisionEngine._analyze_macd(last)
        score += macd_score
        reasons.extend(macd_reasons)
        
        # Determine signal
        if score >= DecisionEngine.BUY_THRESHOLD:
            signal = Recommendation.BUY.value
        elif score <= DecisionEngine.SELL_THRESHOLD:
            signal = Recommendation.SELL.value
        else:
            signal = Recommendation.HOLD.value
        
        # Confidence: normalized absolute score
        confidence = min(abs(score), 100)
        
        # Entry price
        entry = round(last["close"], 2)
        
        # ATR-based levels
        atr = round(last["ATR"], 2)
        stop_loss, target1, target2 = DecisionEngine._calculate_levels(entry, atr, signal)
        
        # Risk-reward ratio
        rr = DecisionEngine._calculate_risk_reward(entry, stop_loss, target1)
        
        return DecisionOutput(
            symbol=symbol,
            signal=signal,
            confidence=confidence,
            entry=entry,
            stop_loss=stop_loss,
            target1=target1,
            target2=target2,
            risk_reward_ratio=rr,
            reasons=reasons,
        )
