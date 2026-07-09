import pandas as pd

from indicators.pipeline import IndicatorPipeline

df = pd.read_csv("data/history/RELIANCE.csv")

df = IndicatorPipeline.run(df)

print(df.tail())