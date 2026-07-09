from market.instruments import InstrumentService

service = InstrumentService()

symbols = [
    "RELIANCE",
    "TCS",
    "INFY",
    "SBIN"
]

for symbol in symbols:
    print(
        symbol,
        "=>",
        service.get_security_id(symbol)
    )