from abc import ABC, abstractmethod

class MarketDataProvider(ABC):

    @abstractmethod
    def get_historical_data(self):
        pass

    @abstractmethod
    def get_live_price(self):
        pass

    @abstractmethod
    def get_option_chain(self):
        pass