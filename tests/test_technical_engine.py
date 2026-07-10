from market.historical import HistoricalService
from indicators.master_pipeline import MasterPipeline
from engine.technical_engine import TechnicalEngine

history = HistoricalService()

df = history.load("NIFTY")

df = MasterPipeline.calculate(df)

state = TechnicalEngine.analyze(

    symbol="NIFTY",

    df=df,

)

print(state)