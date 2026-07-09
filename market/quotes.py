from market.dhan import DhanClient
from market.instruments import InstrumentService


class QuoteService:

    def __init__(self):

        self.client = DhanClient().client
        self.instrument = InstrumentService()

    def get_quote(self, symbol: str):

        info = self.instrument.resolve(symbol)

        if info is None:
            return {
                "status": "error",
                "message": f"{symbol} not found"
            }

        exchange = self.instrument.get_exchange_key(info)

        payload = {
            exchange: [info["security_id"]]
        }

        print("Payload:", payload)

        return self.client.quote_data(payload)