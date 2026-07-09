from dataclasses import dataclass
from datetime import datetime


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