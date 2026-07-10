from core.portfolio import Portfolio
from core.trade import Trade


class PortfolioManager:

    @staticmethod
    def can_open_trade(
        portfolio: Portfolio,
        trade: Trade,
    ) -> bool:

        if len(portfolio.open_trades) >= portfolio.max_positions:
            return False

        if portfolio.today_loss >= portfolio.max_daily_loss:
            return False

        required = trade.entry * trade.quantity

        if required > portfolio.available_capital:
            return False

        return True

    @staticmethod
    def open_trade(
        portfolio: Portfolio,
        trade: Trade,
    ):

        portfolio.open_trades.append(trade)

        investment = trade.entry * trade.quantity

        portfolio.available_capital -= investment

        portfolio.invested_capital += investment

        portfolio.total_trades += 1

        trade.status = "OPEN"

        return portfolio

    @staticmethod
    def close_trade(
        portfolio: Portfolio,
        trade: Trade,
    ):

        if trade not in portfolio.open_trades:
            return portfolio

        portfolio.open_trades.remove(trade)

        portfolio.closed_trades.append(trade)

        investment = trade.entry * trade.quantity

        portfolio.available_capital += investment

        portfolio.invested_capital -= investment

        pnl = trade.pnl

        portfolio.realized_pnl += pnl

        if pnl >= 0:

            portfolio.winning_trades += 1

        else:

            portfolio.losing_trades += 1

            portfolio.today_loss += abs(pnl)

        return portfolio

    @staticmethod
    def statistics(portfolio: Portfolio):

        win_rate = 0

        if portfolio.total_trades:

            win_rate = (

                portfolio.winning_trades

                / portfolio.total_trades

            ) * 100

        return {

            "Capital": portfolio.capital,

            "Available": portfolio.available_capital,

            "Invested": portfolio.invested_capital,

            "Realized PnL": portfolio.realized_pnl,

            "Open Trades": len(portfolio.open_trades),

            "Closed Trades": len(portfolio.closed_trades),

            "Win Rate": round(win_rate, 2),

        }