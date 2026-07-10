from dataclasses import dataclass, field
from typing import Optional


# ==========================================================
# PRICE
# ==========================================================

@dataclass(slots=True)
class PriceState:

    symbol: str

    datetime: str

    open: float

    high: float

    low: float

    close: float

    volume: float


# ==========================================================
# TREND
# ==========================================================

@dataclass(slots=True)
class TrendState:

    ema20: float

    ema50: float

    ema200: float

    supertrend: str

    adx: float

    direction: str

    strength: str


# ==========================================================
# MOMENTUM
# ==========================================================

@dataclass(slots=True)
class MomentumState:

    rsi: float

    macd: float

    macd_signal: float

    macd_hist: float


# ==========================================================
# VOLATILITY
# ==========================================================

@dataclass(slots=True)
class VolatilityState:

    atr: float

    atr_signal: Optional[str] = None


# ==========================================================
# VOLUME
# ==========================================================

@dataclass(slots=True)
class VolumeState:

    vwap_signal: str

    volume_signal: Optional[str] = None

    # ==========================================================
# MARKET STRUCTURE
# ==========================================================

@dataclass(slots=True)
class StructureState:

    bos: Optional[str] = None

    choch: Optional[str] = None

    supports: list[float] = field(default_factory=list)

    resistances: list[float] = field(default_factory=list)


# ==========================================================
# SMART MONEY
# ==========================================================

@dataclass(slots=True)
class SmartMoneyState:

    bullish_order_blocks: list[float] = field(default_factory=list)

    bearish_order_blocks: list[float] = field(default_factory=list)

    bullish_fvgs: list[float] = field(default_factory=list)

    bearish_fvgs: list[float] = field(default_factory=list)

    buy_side_liquidity: list[float] = field(default_factory=list)

    sell_side_liquidity: list[float] = field(default_factory=list)

    liquidity_sweeps: list[float] = field(default_factory=list)

    mitigated_blocks: list[float] = field(default_factory=list)


# ==========================================================
# SCORES
# ==========================================================

@dataclass(slots=True)
class ScoreState:

    trend_score: int

    momentum_score: int

    volume_score: int

    volatility_score: int

    structure_score: int

    technical_score: int

    confidence: str


# ==========================================================
# COMPLETE MARKET STATE
# ==========================================================

@dataclass(slots=True)
class MarketState:

    price: PriceState

    trend: TrendState

    momentum: MomentumState

    volatility: VolatilityState

    volume: VolumeState

    structure: StructureState

    smart_money: SmartMoneyState

    score: ScoreState