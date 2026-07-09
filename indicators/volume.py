import pandas as pd


class VolumeIndicator:

    @staticmethod
    def calculate(df: pd.DataFrame) -> pd.DataFrame:

        data = df.copy()

        data["VOLUME_COLOR"] = data.apply(
            lambda row: "green"
            if row["close"] >= row["open"]
            else "red",
            axis=1,
        )

        return data