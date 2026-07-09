from market.historical import HistoricalService

service = HistoricalService()

df = service.daily(
    security_id="13",
    exchange_segment="IDX_I",
    instrument_type="INDEX",
    from_date="2026-06-01",
    to_date="2026-07-08"
)

print("=" * 60)

print(df)

print("=" * 60)

print(df.columns)