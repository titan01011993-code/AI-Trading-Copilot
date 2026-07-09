from dhanhq import DhanContext, dhanhq
from app.settings import settings
from loguru import logger


class DhanClient:

    def __init__(self):

        self.context = DhanContext(
            settings.DHAN_CLIENT_ID,
            settings.DHAN_ACCESS_TOKEN
        )

        self.client = dhanhq(self.context)

        logger.success("Dhan Client Initialized")

    def get_fund_limits(self):
        try:
            return self.client.get_fund_limits()
        except Exception as e:
            logger.exception(e)
            return None