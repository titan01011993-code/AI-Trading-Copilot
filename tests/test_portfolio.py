from core.portfolio import Portfolio
from core.trade import Trade
from engine.portfolio_manager import PortfolioManager

portfolio = Portfolio(

    capital=500000,

    available_capital=500000,

)

trade = Trade(

    symbol="NIFTY",

    side="BUY",

    timeframe="1D",

    entry=25000,

    stoploss=24800,

    target1=25300,

    target2=25500,

    target3=25800,

    quantity=75,

    confidence=90,

    strategy="Swing",

)

if PortfolioManager.can_open_trade(

    portfolio,

    trade,

):

    PortfolioManager.open_trade(

        portfolio,

        trade,

    )

print()

print(

    PortfolioManager.statistics(

        portfolio

    )

)