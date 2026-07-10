from market.historical import HistoricalService
from indicators.master_pipeline import MasterPipeline
from engine.technical_engine import TechnicalEngine

history = HistoricalService()

df = history.load("NIFTY")

df = MasterPipeline.calculate(df)

result = TechnicalEngine.analyze(df)

print()

print("=" * 60)
print("AI TRADING COPILOT")
print("=" * 60)

for k, v in result.items():
    print(f"{k:<20}: {v}")

print("=" * 60)