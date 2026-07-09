import pandas as pd
import yfinance as yf

from market.providers.base import BaseProvider


class YahooProvider(BaseProvider):
    """
    Yahoo Finance Historical Provider
    """

    def get_history(self, symbol: str) -> pd.DataFrame:

        ticker = f"{symbol.upper()}.NS"

        df = yf.download(
            ticker,
            period="6mo",
            interval="1d",
            progress=False,
            auto_adjust=False,
        )

        if df.empty:
            raise ValueError(f"No data found for {symbol}")

        # Handle new yfinance MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Move Date index into a column
        df = df.reset_index()

        # Standardize column names
        df.columns = [str(c).lower() for c in df.columns]

        # Rename date -> datetime
        df.rename(
            columns={
                "date": "datetime"
            },
            inplace=True
        )

        # Keep only required columns
        df = df[
            [
                "datetime",
                "open",
                "high",
                "low",
                "close",
                "volume",
            ]
        ]

        return df