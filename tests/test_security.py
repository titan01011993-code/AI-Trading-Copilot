from market.instruments import InstrumentService

service = InstrumentService()

print("=" * 50)

print(service.get_symbol("RELIANCE"))

print("=" * 50)

print(service.get_security_id("RELIANCE"))