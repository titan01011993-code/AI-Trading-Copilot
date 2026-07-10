from market.historical import HistoricalService

from indicators.master_pipeline import MasterPipeline

from engine.signal_engine import SignalEngine


history = HistoricalService()

df = history.load("NIFTY")

df = MasterPipeline.calculate(df)

signal = SignalEngine.generate(df)

print()

print("=" * 60)

print("AI SIGNAL ENGINE")

print("=" * 60)

for k, v in signal.items():

    print(f"{k:<15}: {v}")

print("=" * 60)