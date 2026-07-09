from market.instruments import InstrumentService

service = InstrumentService()

print("=" * 60)

print(service.get_symbol("RELIANCE"))

print("=" * 60)

print(service.get_security_id("RELIANCE"))