from __future__ import annotations
import logging

_FMT = "%(asctime)s [%(levelname)s] kona::%(name)s: %(message)s"


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_FMT))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
