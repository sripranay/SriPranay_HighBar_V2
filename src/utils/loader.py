# src/utils/loader.py
from __future__ import annotations
from pathlib import Path
import pandas as pd
import logging
from typing import Any, Dict, Union

LOG = logging.getLogger(__name__)


def load_data(path_or_cfg: Union[str, Path, Dict[str, Any], None] = None):
    cfg = {}
    if isinstance(path_or_cfg, dict):
        cfg = path_or_cfg
    elif isinstance(path_or_cfg, (str, Path)):
        cfg = {"path": str(path_or_cfg)}

    path = cfg.get("path")
    if path:
        p = Path(path)
        if not p.exists():
            LOG.error("Data file not found: %s", p)
            return pd.DataFrame()
        try:
            df = pd.read_csv(p)
            return df
        except Exception as e:
            LOG.exception("Could not read csv %s: %s", p, e)
            return pd.DataFrame()

    for folder in ("data", "data/"):
        p = Path(folder)
        if p.exists():
            files = list(p.glob("*.csv"))
            if files:
                try:
                    return pd.read_csv(files[0])
                except Exception as e:
                    LOG.exception("Could not read csv %s: %s", files[0], e)
                    return pd.DataFrame()
    LOG.warning("No data file found; returning empty DataFrame")
    return pd.DataFrame()
