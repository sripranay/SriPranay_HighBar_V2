# src/agents.insight.py
from __future__ import annotations
import logging
from typing import Any, Dict, List
import pandas as pd

LOG = logging.getLogger(__name__)


def insight_agent(df: pd.DataFrame, evaluated_hypotheses: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"insights": [], "meta": {"rows": getattr(df, "shape", (0, 0))[0]}}
