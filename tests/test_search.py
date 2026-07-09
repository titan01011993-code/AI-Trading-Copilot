from market.instruments import InstrumentService

service = InstrumentService()

result = service.search("RELI")

print(result[
    [
        "SM_SYMBOL_NAME",
        "SEM_TRADING_SYMBOL",
        "SEM_CUSTOM_SYMBOL",
        "SEM_SMST_SECURITY_ID",
        "SEM_SEGMENT",
    ]
].head(30))