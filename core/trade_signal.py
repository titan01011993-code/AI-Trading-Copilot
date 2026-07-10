from dataclasses import dataclass, field


@dataclass
class TradeSignal:

    symbol: str

    signal: str

    timeframe: str

    confidence: float

    entry: float

    stoploss: float

    target1: float

    target2: float

    target3: float

    risk_reward: float

    score: float

    reasons: list[str] = field(default_factory=list)

    generated_at: str = ""