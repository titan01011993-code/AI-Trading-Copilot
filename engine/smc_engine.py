from indicators.swing import SwingIndicator
from indicators.bos import BOSIndicator
from indicators.choch import CHOCHIndicator
from indicators.support_resistance import SupportResistanceIndicator
from indicators.order_block import OrderBlockIndicator
from indicators.fair_value_gap import FairValueGapIndicator
from indicators.liquidity import LiquidityIndicator
from indicators.liquidity_sweep import LiquiditySweepIndicator
from indicators.mitigation import MitigationIndicator


class SMCEngine:

    @staticmethod
    def calculate(df):

        df = SwingIndicator.calculate(df)

        df = BOSIndicator.calculate(df)

        df = CHOCHIndicator.calculate(df)

        df = SupportResistanceIndicator.calculate(df)

        df = OrderBlockIndicator.calculate(df)

        df = FairValueGapIndicator.calculate(df)

        df = LiquidityIndicator.calculate(df)

        df = LiquiditySweepIndicator.calculate(df)

        df = MitigationIndicator.calculate(df)

        return df