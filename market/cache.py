from pathlib import Path
import pandas as pd


class DataCache:

    def __init__(self):

        self.folder = Path("data/cache")
        self.folder.mkdir(parents=True, exist_ok=True)

    def save(self, name: str, df: pd.DataFrame):

        df.to_csv(self.folder / f"{name}.csv", index=False)

    def load(self, name: str):

        file = self.folder / f"{name}.csv"

        if file.exists():
            return pd.read_csv(file)

        return pd.DataFrame()