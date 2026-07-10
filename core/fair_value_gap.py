from dataclasses import dataclass


@dataclass
class FairValueGap:

    upper: float

    lower: float

    direction: str

    filled: bool = False

    created_at: str = ""

    timeframe: str = "1D"