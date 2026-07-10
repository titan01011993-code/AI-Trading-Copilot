from features.trend_features import TrendFeatures
from features.momentum_features import MomentumFeatures
from features.volume_features import VolumeFeatures
from features.volatility_features import VolatilityFeatures
from features.structure_features import StructureFeatures
from features.smart_money_features import SmartMoneyFeatures


class FeatureEngine:

    @staticmethod
    def calculate(df):

        df = TrendFeatures.calculate(df)

        df = MomentumFeatures.calculate(df)

        df = VolumeFeatures.calculate(df)

        df = VolatilityFeatures.calculate(df)

        df = StructureFeatures.calculate(df)

        df = SmartMoneyFeatures.calculate(df)

        return df