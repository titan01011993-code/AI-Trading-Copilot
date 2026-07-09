from datetime import datetime
import pandas as pd
from loguru import logger

from market.dhan import DhanClient


class HistoricalService:

    def __init__(self):
        self.client = DhanClient().client

    def daily(
        self,
        security_id: str,
        exchange_segment: str,
        instrument_type: str,
        from_date: str,
        to_date: str,
        expiry_code: int = 0,
        oi: bool = False,
    ) -> pd.DataFrame:

        try:

            response = self.client.historical_daily_data(
                security_id=security_id,
                exchange_segment=exchange_segment,
                instrument_type=instrument_type,
                from_date=from_date,
                to_date=to_date,
                expiry_code=expiry_code,
                oi=oi,
            )

            logger.info("Historical data received")

            return self._to_dataframe(response)

        except Exception as e:
            logger.exception(e)
            return pd.DataFrame()

    def _to_dataframe(self, response):

        if not response:
            return pd.DataFrame()

        # We will inspect the response format first.
        return pd.DataFrame(response)
    
    import pandas as pd


class HistoricalService:

    def load_csv(self, path):

        df = pd.read_csv(path)

        df.columns = [
            c.lower()
            for c in df.columns
        ]

        return df