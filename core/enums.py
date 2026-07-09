from enum import Enum


class Trend(Enum):

    BULLISH = "Bullish"

    BEARISH = "Bearish"

    SIDEWAYS = "Sideways"


class Recommendation(Enum):

    BUY = "BUY"

    SELL = "SELL"

    HOLD = "HOLD"