"""
Master Indicator Pipeline

Runs every indicator in the correct order.

Flow

Historical Data
    ↓
Basic Indicators
    ↓
Trend / Momentum
    ↓
Smart Money Concepts
    ↓
Technical Score
"""

from indicators.pipeline import IndicatorPipeline
from indicators.swing import SwingIndicator
from indicators.bos import BOSIndicator
from indicators.choch import CHOCHIndicator
from indicators.support_resistance import SupportResistanceIndicator
from indicators.order_block import OrderBlockIndicator
from indicators.fair_value_gap import FairValueGapIndicator
from indicators.liquidity import LiquidityIndicator
from indicators.liquidity_sweep import LiquiditySweepIndicator
from indicators.mitigation import MitigationIndicator
from indicators.technical_score import TechnicalScore


class MasterPipeline:

    @staticmethod
    def calculate(df):

        # ======================================
        # BASIC INDICATORS
        # ======================================

        df = IndicatorPipeline.calculate(df)

        # ======================================
        # MARKET STRUCTURE
        # ======================================

        df = SwingIndicator.calculate(df)

        df = BOSIndicator.calculate(df)

        df = CHOCHIndicator.calculate(df)

        df = SupportResistanceIndicator.calculate(df)

        # ======================================
        # SMART MONEY
        # ======================================

        df = OrderBlockIndicator.calculate(df)

        df = FairValueGapIndicator.calculate(df)

        df = LiquidityIndicator.calculate(df)

        df = LiquiditySweepIndicator.calculate(df)

        df = MitigationIndicator.calculate(df)

        # ======================================
        # FINAL TECHNICAL SCORE
        # ======================================

        df = TechnicalScore.calculate(df)

        return df