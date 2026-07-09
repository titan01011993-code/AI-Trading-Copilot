from market.instruments import InstrumentService

service = InstrumentService()

print("=" * 80)
print(service.search("NIFTY").head(20))
print("=" * 80)

print(service.search("BANK").head(20))