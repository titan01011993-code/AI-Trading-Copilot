import pandas as pd


class DataValidator:
    """
    Enterprise Data Validation Layer

    Responsibilities
    ----------------
    • Standardize columns
    • Convert datetime
    • Convert numeric columns
    • Remove duplicates
    • Remove invalid OHLC rows
    • Remove NaN
    • Sort candles
    • Remove incomplete candles
    """

    REQUIRED_COLUMNS = [

        "datetime",

        "open",

        "high",

        "low",

        "close",

        "volume",

    ]

    NUMERIC_COLUMNS = [

        "open",

        "high",

        "low",

        "close",

        "volume",

    ]

    @classmethod
    def validate(

        cls,

        df: pd.DataFrame,

        timeframe: str = "1D",

    ) -> pd.DataFrame:

        if df.empty:

            raise ValueError("Historical dataframe is empty.")

        # -------------------------------------
        # Required Columns
        # -------------------------------------

        missing = [

            c

            for c in cls.REQUIRED_COLUMNS

            if c not in df.columns

        ]

        if missing:

            raise ValueError(

                f"Missing columns : {missing}"

            )

        # -------------------------------------
        # Datetime
        # -------------------------------------

        df["datetime"] = pd.to_datetime(

            df["datetime"],

            errors="coerce",

        )

        # -------------------------------------
        # Numeric
        # -------------------------------------

        df[cls.NUMERIC_COLUMNS] = (

            df[cls.NUMERIC_COLUMNS]

            .apply(

                pd.to_numeric,

                errors="coerce",

            )

        )

        # -------------------------------------
        # Remove Invalid Rows
        # -------------------------------------

        df = df.dropna()

        # -------------------------------------
        # Remove duplicate candles
        # -------------------------------------

        df = df.drop_duplicates(

            subset="datetime",

            keep="last",

        )

        # -------------------------------------
        # Sort candles
        # -------------------------------------

        df = (

            df

            .sort_values("datetime")

            .reset_index(drop=True)

        )

        # -------------------------------------
        # Remove impossible candles
        # -------------------------------------

        df = df[

            (df["high"] >= df["open"])

            &

            (df["high"] >= df["close"])

            &

            (df["low"] <= df["open"])

            &

            (df["low"] <= df["close"])

            &

            (df["high"] >= df["low"])

        ]

        # -------------------------------------
        # Remove incomplete candle
        # -------------------------------------
        if len(df):
            last = df.iloc[-1]

            if (
                pd.isna(last["volume"]) or last["volume"] <= 0
            ):
                df = df.iloc[:-1]

        # -------------------------------------
        # Final Reset
        # -------------------------------------

        df = df.reset_index(drop=True)

        return df