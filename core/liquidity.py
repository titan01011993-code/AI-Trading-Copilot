from dataclasses import dataclass


@dataclass
class LiquidityZone:

    level: float

    side: str

    touches: int

    swept: bool = False

    active: bool = True

    created_at: str = ""

    timeframe: str = "1D"