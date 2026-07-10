from market.providers.yahoo_provider import YahooProvider


class HistoricalService:

    def __init__(self):

        self.provider = YahooProvider()

    def load(

        self,

        symbol: str,

        timeframe: str = "1D",

        period: str | None = None,

    ):

        return self.provider.get_history(

            symbol=symbol,

            timeframe=timeframe,

            period=period,

        )