from market.providers.base import BaseProvider


class DhanProvider(BaseProvider):

    def get_history(self, symbol: str):
        raise NotImplementedError(
            "Dhan historical provider coming soon."
        )