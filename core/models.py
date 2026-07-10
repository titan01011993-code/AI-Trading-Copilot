from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass(slots=True)
class Candle:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass(slots=True)
class Quote:
    symbol: str
    security_id: int
    ltp: float
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass(slots=True)
class Signal:
    symbol: str
    trend: str
    recommendation: str
    score: float
    confidence: float
    stop_loss: float
    target: float


@dataclass(slots=True)
class DecisionOutput:
    """
    Complete decision output from DecisionEngine.
    Contains signal recommendation, price levels, and risk metrics.
    """
    symbol: str
    signal: str  # BUY, SELL, HOLD
    confidence: float  # 0-100
    entry: float
    stop_loss: float
    target1: float
    target2: float
    risk_reward_ratio: float
    reasons: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_signal(self, trend: str) -> Signal:
        """Convert DecisionOutput to Signal dataclass."""
        return Signal(
            symbol=self.symbol,
            trend=trend,
            recommendation=self.signal,
            score=self.confidence,
            confidence=self.confidence,
            stop_loss=self.stop_loss,
            target=self.target1,
        )
