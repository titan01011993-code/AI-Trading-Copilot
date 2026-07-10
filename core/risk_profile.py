from dataclasses import dataclass


@dataclass
class RiskProfile:

    capital: float

    risk_percent: float

    max_daily_loss: float

    max_open_trades: int

    lot_size: int

    brokerage: float

    slippage: float

    leverage: float = 1