from loguru import logger

logger.add(
    "logs/trading.log",
    rotation="10 MB",
    retention="30 days",
    level="INFO"
)

logger.info("Logger Initialized")