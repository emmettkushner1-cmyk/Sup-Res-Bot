from __future__ import annotations

import logging
from typing import Optional

from .config import Config


def configure_logging(config: Config, logger_name: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    if logger.handlers:
        return logger

    level = getattr(logging, config.log_level.upper(), logging.INFO)
    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(level)
    logger.addHandler(handler)

    logger.propagate = False
    return logger
