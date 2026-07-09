from market.dhan import DhanClient

client = DhanClient().client

response = client.fetch_security_list()

print(response)