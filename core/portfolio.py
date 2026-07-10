from dataclasses import dataclass, field
from core.trade import Trade


@dataclass
class Portfolio:

    capital: float

    available_capital: float

    invested_capital: float = 0

    unrealized_pnl: float = 0

    realized_pnl: float = 0

    open_trades: list[Trade] = field(default_factory=list)

    closed_trades: list[Trade] = field(default_factory=list)

    max_positions: int = 5

    max_daily_loss: float = 5000

    today_loss: float = 0

    total_trades: int = 0

    winning_trades: int = 0

    losing_trades: int = 0