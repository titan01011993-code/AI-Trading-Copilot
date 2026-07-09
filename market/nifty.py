from market.historical import HistoricalService


class NiftyService:

    def __init__(self):
        self.history = HistoricalService()

    def load(self):
        return self.history.load("^NSEI")