from dataclasses import dataclass


@dataclass
class Alignment:

    bullish: int

    bearish: int

    neutral: int

    alignment_score: float

    direction: str