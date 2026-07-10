from dataclasses import dataclass, field


@dataclass(slots=True)
class DecisionState:
    """
    AI Decision Output
    """

    buy_score: int

    sell_score: int

    hold_score: int

    bias: str

    confidence: int

    reasons: list[str] = field(default_factory=list)