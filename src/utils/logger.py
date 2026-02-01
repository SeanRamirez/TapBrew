"""Logging configuration for TapFlow."""

import logging
import sys
from typing import Optional

from .config import get_settings


def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """Configure and return a logger instance.

    Args:
        name: Logger name. If None, returns the root logger.

    Returns:
        Configured logger instance.
    """
    settings = get_settings()

    logger = logging.getLogger(name or "tapflow")
    logger.setLevel(getattr(logging, settings.log_level.upper()))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, settings.log_level.upper()))

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


# Default logger instance
logger = setup_logger()
