import pandas as pd
from loguru import logger

from market.dhan import DhanClient


class InstrumentService:
    """
    Handles all security lookup operations.
    Loads the Dhan security master only once.
    """

    _master = None

    def __init__(self):

        self.client = DhanClient().client

        if InstrumentService._master is None:

            logger.info("Loading Security Master...")

            InstrumentService._master = self.client.fetch_security_list()

            logger.success(
                f"{len(InstrumentService._master)} instruments loaded."
            )

        self.df = InstrumentService._master

    def search(self, text: str):

        text = text.upper()

        mask = (
            self.df["SM_SYMBOL_NAME"].astype(str).str.upper().str.contains(text, na=False)
            |
            self.df["SEM_TRADING_SYMBOL"].astype(str).str.upper().str.contains(text, na=False)
            |
            self.df["SEM_CUSTOM_SYMBOL"].astype(str).str.upper().str.contains(text, na=False)
        )

        return self.df[mask]

    def resolve(self, symbol: str):

        symbol = symbol.upper()

        exact = self.df[
            (self.df["SEM_TRADING_SYMBOL"].astype(str).str.upper() == symbol)
            &
            (self.df["SEM_EXM_EXCH_ID"] == "NSE")
            &
            (self.df["SEM_INSTRUMENT_NAME"] == "EQUITY")
        ]

        if exact.empty:
            exact = self.search(symbol)

        if exact.empty:
            return None

        row = exact.iloc[0]

        return {
            "symbol": row["SEM_TRADING_SYMBOL"],
            "company": row["SM_SYMBOL_NAME"],
            "security_id": int(row["SEM_SMST_SECURITY_ID"]),
            "exchange": row["SEM_EXM_EXCH_ID"],
            "segment": row["SEM_SEGMENT"],
            "instrument": row["SEM_INSTRUMENT_NAME"],
            "series": row["SEM_SERIES"],
        }

    def get_exchange_key(self, instrument):

        if instrument["exchange"] == "NSE" and instrument["instrument"] == "EQUITY":
            return "NSE_EQ"

        if instrument["exchange"] == "BSE" and instrument["instrument"] == "EQUITY":
            return "BSE_EQ"

        if instrument["instrument"] == "INDEX":
            return "IDX_I"

        return None