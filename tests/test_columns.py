from market.dhan import DhanClient

client = DhanClient().client

df = client.fetch_security_list()

print(df.columns.tolist())