from core.market_state import MarketState
from core.trade_signal import TradeSignal
from core.risk_profile import RiskProfile


class RiskEngine:

    @staticmethod
    def calculate(
        state: MarketState,
        signal: TradeSignal,
        profile: RiskProfile,
    ):

        if signal.signal == "WAIT":

            return {

                "POSITION_SIZE": 0,

                "CAPITAL_AT_RISK": 0,

                "LOTS": 0,

                "EXPECTED_PROFIT_T1": 0,

                "EXPECTED_PROFIT_T2": 0,

                "EXPECTED_PROFIT_T3": 0,

            }

        risk_per_share = abs(

            signal.entry - signal.stoploss

        )

        capital_risk = (

            profile.capital

            * profile.risk_percent

            / 100

        )

        quantity = int(

            capital_risk / risk_per_share

        )

        lots = max(

            quantity // profile.lot_size,

            1,

        )

        quantity = lots * profile.lot_size

        expected_profit_t1 = (

            abs(signal.target1 - signal.entry)

            * quantity

        )

        expected_profit_t2 = (

            abs(signal.target2 - signal.entry)

            * quantity

        )

        expected_profit_t3 = (

            abs(signal.target3 - signal.entry)

            * quantity

        )

        return {

            "POSITION_SIZE": quantity,

            "LOTS": lots,

            "CAPITAL_AT_RISK": round(capital_risk, 2),

            "EXPECTED_PROFIT_T1": round(expected_profit_t1, 2),

            "EXPECTED_PROFIT_T2": round(expected_profit_t2, 2),

            "EXPECTED_PROFIT_T3": round(expected_profit_t3, 2),

        }