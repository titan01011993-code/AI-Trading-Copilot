from market.dhan import DhanClient


class OHLCService:

    def __init__(self):
        self.client = DhanClient().client

    def ohlc(
        self,
        security_id,
        exchange_segment
    ):

        return self.client.ohlc_data(
            security_id=security_id,
            exchange_segment=exchange_segment
        )