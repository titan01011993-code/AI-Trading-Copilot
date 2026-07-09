from market.live import LiveMarket

market = LiveMarket()

print("=" * 60)
print("LIVE MARKET TEST")
print("=" * 60)

print(market.get_fund_limits())