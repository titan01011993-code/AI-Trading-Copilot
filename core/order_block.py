from dataclasses import dataclass


@dataclass
class OrderBlock:

    high: float

    low: float

    direction: str

    created_at: str

    mitigated: bool = False

    strength: float = 0

    timeframe: str = "1D"