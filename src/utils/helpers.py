# src/utils.helpers.py
from __future__ import annotations
from pathlib import Path
import json
import logging
from typing import Any, Dict, Union

LOG = logging.getLogger(__name__)


def load_schema(path_or_dict: Union[str, Path, Dict[str, Any]]) -> Union[Dict[str, Any], bool]:
    if isinstance(path_or_dict, dict):
        return path_or_dict
    p = Path(path_or_dict)
    if not p.exists():
        LOG.warning("Schema file not found: %s", p)
        return False
    with p.open("r", encoding="utf8") as fh:
        return json.load(fh)


def compute_kpis(df) -> Dict[str, Any]:
    if df is None:
        return {}
    try:
        rows = getattr(df, "shape", (0, 0))[0]
        return {"rows": rows}
    except Exception:
        return {}
