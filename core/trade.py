from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Trade:

    symbol: str

    side: str

    timeframe: str

    entry: float

    stoploss: float

    target1: float

    target2: float

    target3: float

    quantity: int

    confidence: float

    strategy: str

    status: str = "PENDING"

    current_price: float = 0.0

    exit_price: Optional[float] = None

    pnl: float = 0.0

    rr: float = 0.0

    opened_at: datetime = field(default_factory=datetime.now)

    closed_at: Optional[datetime] = None

    target1_hit: bool = False

    target2_hit: bool = False

    target3_hit: bool = False

    trailing_stop: Optional[float] = None

    notes: str = ""