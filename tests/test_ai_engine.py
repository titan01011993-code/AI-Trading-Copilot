from engine.ai_engine import AIEngine

from core.risk_profile import RiskProfile


profile = RiskProfile(

    capital=100000,

    risk_percent=1,

    lot_size=75,

)

engine = AIEngine()

result = engine.analyze(

    "NIFTY",

    profile,

)

print()

print("=" * 70)

print("           AI TRADING COPILOT")

print("=" * 70)

print()

print("MARKET STATE")

print(result["market_state"])

print()

print("SIGNAL")

print(result["trade_signal"])

print()

print("RISK")

print(result["risk"])

print()

print("=" * 70)