from market.historical import HistoricalService

from ai.market_structure import MarketStructure

history = HistoricalService()

df = history.load("RELIANCE")

result = MarketStructure.analyze(df)

print(result)