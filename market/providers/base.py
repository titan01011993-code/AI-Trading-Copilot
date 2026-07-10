from abc import ABC, abstractmethod
import pandas as pd


class BaseProvider(ABC):

    @abstractmethod
    def get_history(
        self,
        symbol: str,
        timeframe: str = "1D",
        period: str | None = None,
    ) -> pd.DataFrame:
        pass