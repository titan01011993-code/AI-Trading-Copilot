from market.providers.yahoo_provider import YahooProvider


class HistoricalService:

    def __init__(self):

        self.provider = YahooProvider()

    def load(self, symbol):

        return self.provider.get_history(symbol)