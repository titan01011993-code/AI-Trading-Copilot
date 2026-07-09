# tests/test_dhan_quote_direct.py

from market.dhan import DhanClient
from pprint import pprint

client = DhanClient().client

payload = {
    "NSE_EQ": [2885]
}

print("Payload:", payload)

response = client.quote_data(payload)

pprint(response)