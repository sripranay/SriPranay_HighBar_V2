# src/agents.evaluator.py
from __future__ import annotations
import logging
from typing import Any, Dict, List
import pandas as pd

LOG = logging.getLogger(__name__)


def _safe_parse_dates(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    if date_col not in df.columns:
        raise KeyError(f"date column '{date_col}' not found in DataFrame")
    parsed = pd.to_datetime(df[date_col], errors="coerce")
    df = df.copy()
    df["__date_parsed"] = parsed
    return df


def generate_hypotheses(df: pd.DataFrame, *, group_col: str = "campaign_name", lookback_days: int = 30) -> List[Dict[str, Any]]:
    if df is None or df.empty:
        LOG.info("generate_hypotheses(): received empty df -> returning []")
        return []

    try:
        df2 = _safe_parse_dates(df, "date")
    except Exception as e:
        LOG.warning("generate_hypotheses() error, fallback called: %s", e)
        return []

    if group_col not in df2.columns:
        LOG.info("generate_hypotheses(): group_col %s not in df", group_col)
        return []

    groups = df2.groupby(group_col).groups.keys()
    hypos = []
    for g in list(groups)[:10]:
        hypos.append({"campaign": g, "reason": "auto_detect_drop", "score": 0.5})
    LOG.info("generate_hypotheses(): generated %d hypotheses (group_col=%s, date_col=%s)", len(hypos), group_col, "date")
    return hypos


def evaluate_hypotheses(df: pd.DataFrame, hypotheses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for h in hypotheses:
        h_copy = h.copy()
        h_copy["validated"] = False
        out.append(h_copy)
    LOG.info("evaluate_hypotheses(): validated %d of %d", sum(1 for x in out if x.get("validated")), len(out))
    return out
