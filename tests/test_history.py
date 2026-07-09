from market.historical import HistoricalService

history = HistoricalService()

df = history.load("RELIANCE")

print(df.head())
print()
print(df.tail())
print()
print(df.columns)
print()
print(df.shape)