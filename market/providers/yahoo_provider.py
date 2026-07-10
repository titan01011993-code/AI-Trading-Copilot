import pandas as pd
import yfinance as yf

from market.providers.base import BaseProvider
from market.data_validator import DataValidator

class YahooProvider(BaseProvider):
    """
    Yahoo Finance Historical Provider

    Supports:
        5m
        15m
        30m
        1H
        4H
        1D
        1W
        1M
    """

    INDEX_MAP = {

        "NIFTY": "^NSEI",
        "NIFTY50": "^NSEI",
        "^NSEI": "^NSEI",

        "BANKNIFTY": "^NSEBANK",
        "BANK NIFTY": "^NSEBANK",
        "^NSEBANK": "^NSEBANK",

    }

    TIMEFRAME_MAP = {

        "5m": ("5m", "60d"),

        "15m": ("15m", "60d"),

        "30m": ("30m", "60d"),

        "1H": ("60m", "730d"),

        "4H": ("60m", "730d"),

        "1D": ("1d", "2y"),

        "1W": ("1wk", "5y"),

        "1M": ("1mo", "10y"),

    }

    def get_history(

        self,

        symbol: str,

        timeframe: str = "1D",

        period: str | None = None,

    ) -> pd.DataFrame:

        symbol = symbol.upper().strip()

        ticker = self.INDEX_MAP.get(
            symbol,
            f"{symbol}.NS",
        )

        interval, default_period = self.TIMEFRAME_MAP.get(

            timeframe,

            ("1d", "2y"),

        )

        if period is None:

            period = default_period

        try:

            df = yf.download(

                ticker,

                period=period,

                interval=interval,

                auto_adjust=False,

                progress=False,

                threads=False,

            )

        except Exception as e:

            raise RuntimeError(

                f"Yahoo download failed : {e}"

            )

        if df.empty:

            raise ValueError(

                f"No data found for {symbol}"

            )

        # --------------------------------------------------
        # Flatten MultiIndex
        # --------------------------------------------------

        if isinstance(df.columns, pd.MultiIndex):

            df.columns = df.columns.get_level_values(0)

        # --------------------------------------------------

        df = df.reset_index()

        df.columns = [

            str(c).lower()

            for c in df.columns

        ]

        # --------------------------------------------------
        # Rename datetime column
        # --------------------------------------------------

        if "date" in df.columns:

            df.rename(

                columns={

                    "date": "datetime"

                },

                inplace=True,

            )

        elif "datetime" not in df.columns:

            df.rename(

                columns={

                    df.columns[0]: "datetime"

                },

                inplace=True,

            )

        # --------------------------------------------------
        # Datetime conversion
        # --------------------------------------------------

        df["datetime"] = pd.to_datetime(

            df["datetime"]

        )

        # --------------------------------------------------
        # Numeric conversion
        # --------------------------------------------------

        numeric_columns = [

            "open",

            "high",

            "low",

            "close",

            "volume",

        ]

        df[numeric_columns] = (

            df[numeric_columns]

            .apply(

                pd.to_numeric,

                errors="coerce",

            )

        )

        # --------------------------------------------------
        # 4H Resampling
        # --------------------------------------------------

        if timeframe == "4H":

            df = (

                df

                .set_index("datetime")

                .resample(

                    "4h",

                    label="right",

                    closed="right",

                )

                .agg(

                    {

                        "open": "first",

                        "high": "max",

                        "low": "min",

                        "close": "last",

                        "volume": "sum",

                    }

                )

                .dropna()

                .reset_index()

            )

        # --------------------------------------------------
        # Keep Required Columns
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Clean Dataset
        # --------------------------------------------------

        df = DataValidator.validate(

            df,

            timeframe,

        )

        # --------------------------------------------------
        # Remove incomplete candles
        # --------------------------------------------------

        if timeframe != "1D":

            df = df[df["volume"] > 0]

        return df