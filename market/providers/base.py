from abc import ABC, abstractmethod
import pandas as pd


class BaseProvider(ABC):
    """
    Base class for all market data providers.
    """

    @abstractmethod
    def get_history(self, symbol: str) -> pd.DataFrame:
        """
        Return historical OHLCV data.
        """
        raise NotImplementedError