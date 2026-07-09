from pprint import pprint
from market.dhan import DhanClient

client = DhanClient().client

try:
    response = client.expiry_list(
        under_security_id=13,
        under_exchange_segment="IDX_I"
    )

    pprint(response)

except Exception as e:
    print(e)