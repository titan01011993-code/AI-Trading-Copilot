from abc import ABC
from abc import abstractmethod


class BaseBroker(ABC):

    @abstractmethod
    def get_quote(self, symbol):
        ...

    @abstractmethod
    def get_history(self, symbol):
        ...

    @abstractmethod
    def place_order(self):
        ...

    @abstractmethod
    def positions(self):
        ...