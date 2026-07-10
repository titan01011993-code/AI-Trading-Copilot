from core.trade import Trade
from engine.trade_manager import TradeManager

trade = Trade(

    symbol="NIFTY",

    side="BUY",

    timeframe="1D",

    entry=25000,

    stoploss=24800,

    target1=25200,

    target2=25400,

    target3=25600,

    quantity=75,

    confidence=91,

    strategy="Swing"

)

prices = [

    25050,

    25120,

    25220,

    25300,

    25420,

    25550,

    25650

]

for p in prices:

    trade = TradeManager.update(trade, p)

    print()

    print("--------------------------------")

    print("PRICE :", p)

    print("STATUS :", trade.status)

    print("TRAIL :", trade.trailing_stop)

    print("T1 :", trade.target1_hit)

    print("T2 :", trade.target2_hit)

    print("T3 :", trade.target3_hit)