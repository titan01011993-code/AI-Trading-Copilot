from market.historical import HistoricalService

from indicators.master_pipeline import MasterPipeline

from engine.technical_engine import TechnicalEngine
from engine.signal_engine import SignalEngine
from engine.risk_engine import RiskEngine

from core.risk_profile import RiskProfile


class AIEngine:
    """
    AI Trading Copilot Engine

    Complete Flow

    Historical
        ↓
    Indicators
        ↓
    Technical Engine
        ↓
    Signal Engine
        ↓
    Risk Engine
    """

    def __init__(self):

        self.history = HistoricalService()

    def analyze(

        self,

        symbol: str,

        profile: RiskProfile,

    ):

        # -------------------------
        # Historical Data
        # -------------------------

        df = self.history.load(symbol)

        # -------------------------
        # Indicators
        # -------------------------

        df = MasterPipeline.calculate(df)

        # -------------------------
        # Technical State
        # -------------------------

        state = TechnicalEngine.analyze(df)

        # -------------------------
        # Trading Signal
        # -------------------------

        signal = SignalEngine.generate(state)

        # -------------------------
        # Risk Management
        # -------------------------

        risk = RiskEngine.calculate(

            state,

            signal,

            profile,

        )

        return {

            "market_state": state,

            "trade_signal": signal,

            "risk": risk,

        }