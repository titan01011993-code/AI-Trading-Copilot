from market.historical import HistoricalService

from indicators.master_pipeline import MasterPipeline

from engine.technical_engine import TechnicalEngine
from engine.signal_engine import SignalEngine
from engine.risk_engine import RiskEngine

from core.risk_profile import RiskProfile


history = HistoricalService()

df = history.load("NIFTY")

df = MasterPipeline.calculate(df)

state = TechnicalEngine.analyze(df)

signal = SignalEngine.generate(state)

profile = RiskProfile(

    capital=100000,

    risk_percent=1,

    lot_size=75,

)

risk = RiskEngine.calculate(

    state,

    signal,

    profile,

)

print()

print("=" * 60)

print("RISK ENGINE")

print("=" * 60)

print(signal)

print()

print(risk)

print("=" * 60)