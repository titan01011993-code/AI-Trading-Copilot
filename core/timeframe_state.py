from dataclasses import dataclass

from core.market_state import MarketState
from core.decision_state import DecisionState


@dataclass
class TimeframeState:

    timeframe: str

    market: MarketState

    decision: DecisionState