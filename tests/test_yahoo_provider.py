from market.providers.yahoo_provider import YahooProvider

provider = YahooProvider()

df = provider.get_history("RELIANCE")

print(df.head())
print()
print(df.columns)
print()
print(df.shape)