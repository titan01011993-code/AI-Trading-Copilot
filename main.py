from market.dhan import DhanClient

print("=" * 50)
print("AI Trading Copilot")
print("=" * 50)

broker = DhanClient()

print("\nConnecting to Dhan...")

response = broker.get_fund_limits()

print(response)