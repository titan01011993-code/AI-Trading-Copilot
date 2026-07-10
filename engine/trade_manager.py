from datetime import datetime


class TradeManager:

    @staticmethod
    def update(trade, current_price):

        trade.current_price = current_price

        # -------------------------
        # BUY
        # -------------------------

        if trade.side == "BUY":

            # Stoploss

            if current_price <= trade.stoploss:

                trade.status = "STOPLOSS"

                trade.exit_price = current_price

                trade.closed_at = datetime.now()

                return trade

            # Target 1

            if (
                current_price >= trade.target1
                and not trade.target1_hit
            ):

                trade.target1_hit = True

                trade.trailing_stop = trade.entry

            # Target 2

            if (
                current_price >= trade.target2
                and not trade.target2_hit
            ):

                trade.target2_hit = True

                trade.trailing_stop = trade.target1

            # Target 3

            if current_price >= trade.target3:

                trade.target3_hit = True

                trade.status = "TARGET HIT"

                trade.exit_price = current_price

                trade.closed_at = datetime.now()

        # -------------------------
        # SELL
        # -------------------------

        else:

            if current_price >= trade.stoploss:

                trade.status = "STOPLOSS"

                trade.exit_price = current_price

                trade.closed_at = datetime.now()

                return trade

            if (
                current_price <= trade.target1
                and not trade.target1_hit
            ):

                trade.target1_hit = True

                trade.trailing_stop = trade.entry

            if (
                current_price <= trade.target2
                and not trade.target2_hit
            ):

                trade.target2_hit = True

                trade.trailing_stop = trade.target1

            if current_price <= trade.target3:

                trade.target3_hit = True

                trade.status = "TARGET HIT"

                trade.exit_price = current_price

                trade.closed_at = datetime.now()

        return trade