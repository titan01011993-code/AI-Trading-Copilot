from loguru import logger

from market.dhan import DhanClient


class LiveMarket:

    def __init__(self):
        self.broker = DhanClient()

    def get_fund_limits(self):
        return self.broker.get_fund_limits()