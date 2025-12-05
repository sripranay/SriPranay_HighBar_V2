# src/agents/planner.py
from __future__ import annotations
import logging
from typing import Any, Dict, List

LOG = logging.getLogger(__name__)


def planner_agent(*, query: str, cfg: Dict[str, Any] | None = None) -> List[str]:
    cfg = cfg or {}
    LOG.info("planner_agent received query: %s", query)
    plan = [
        "load_data",
        "schema_check",
        "compute_kpis",
        "compute_trends",
        "detect_roas_changes",
        "generate_hypotheses",
        "validate_hypotheses",
        "generate_creative_recommendations",
        "compile_report",
    ]
    return plan
