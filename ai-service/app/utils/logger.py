"""
Basic logging configuration shared across the app.
"""
import logging
import sys
from app.config.settings import get_settings


def get_logger(name: str) -> logging.Logger:
    settings = get_settings()
    logger = logging.getLogger(name)

    if not logger.handlers:  # avoid duplicate handlers on reload
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(settings.LOG_LEVEL)

    return logger
