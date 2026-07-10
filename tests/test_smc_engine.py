from market.historical import HistoricalService
from engine.smc_engine import SMCEngine

history = HistoricalService()

df = history.load("NIFTY")

df = SMCEngine.calculate(df)

print(df.tail())