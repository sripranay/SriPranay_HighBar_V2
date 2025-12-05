# src/utils/logger.py
from __future__ import annotations
import logging
from pathlib import Path


def setup_logger(level: str = "INFO", logs_dir: str | Path = "logs") -> logging.Logger:
    logs_dir = Path(logs_dir)
    logs_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # avoid duplicate handlers
    if logger.handlers:
        logger.handlers = []

    timestamp = __import__("datetime").datetime.utcnow().strftime("run_%Y%m%dT%H%M%SZ.log")
    fh = logging.FileHandler(logs_dir / timestamp)
    fh.setLevel(getattr(logging, level.upper(), logging.INFO))

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    fh.setFormatter(formatter)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    return logging.getLogger(name)
