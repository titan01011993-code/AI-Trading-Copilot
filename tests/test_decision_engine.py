from market.historical import HistoricalService

from indicators.master_pipeline import MasterPipeline

from engine.technical_engine import TechnicalEngine
from engine.decision_engine import DecisionEngine

history = HistoricalService()

df = history.load("NIFTY")

df = MasterPipeline.calculate(df)

state = TechnicalEngine.analyze(df)

decision = DecisionEngine.analyze(state)

print()

print("=" * 60)

print("AI DECISION ENGINE")

print("=" * 60)

for k, v in decision.items():

    print(f"{k:<15}: {v}")

print("=" * 60)