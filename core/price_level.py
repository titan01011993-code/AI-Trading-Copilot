from dataclasses import dataclass


@dataclass
class PriceLevel:
    """
    Generic Support / Resistance Level
    """

    price: float

    touches: int = 1

    strength: float = 0.0

    timeframe: str = "1D"

    broken: bool = False

    created_at: str = ""

    last_tested: str = ""