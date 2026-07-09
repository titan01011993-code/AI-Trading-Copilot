from pprint import pprint

from market.dhan import DhanClient

client = DhanClient().client

payload = {
    "NSE_EQ": [2885]
}

http = client.dhan_http

print(type(http))

response = http.post(
    "/marketfeed/quote",
    payload
)

pprint(response)