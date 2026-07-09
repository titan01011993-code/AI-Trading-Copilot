from market.instruments import InstrumentService

service = InstrumentService()

row = service.get_symbol("RELIANCE")

print(row.to_string())