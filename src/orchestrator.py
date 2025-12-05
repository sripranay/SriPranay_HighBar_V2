# src/orchestrator.py
from __future__ import annotations
from pathlib import Path
import logging
from typing import Any, Dict

from src.utils.logger import setup_logger
from src.utils.helpers import load_schema, compute_kpis
from src.utils.loader import load_data

from src.agents.planner import planner_agent
from src.agents.evaluator import evaluate_hypotheses, generate_hypotheses
from src.agents.insight import insight_agent
from src.agents.creative import generate_creatives

LOG = logging.getLogger(__name__)


def _flexible_call(fn, *args, **kwargs):
    """Call a function, allow both positional and keyword-call styles safely."""
    return fn(*args, **kwargs)


def run_pipeline(query: str, cfg: Dict[str, Any] | None = None) -> Dict[str, Any]:
    cfg = cfg or {}
    log_cfg = cfg.get("logging", {})
    setup_logger(level=log_cfg.get("level", "INFO"), logs_dir=log_cfg.get("logs_dir", "logs"))
    LOG.info("run_pipeline: starting (query=%s)", query)

    schema_path = cfg.get("schema", Path("schemas/schema_v1.json"))
    try:
        schema = load_schema(schema_path)
        LOG.info("Loaded schema OK: %s", schema)
    except Exception as e:
        LOG.exception("Schema load failed: %s", e)
        schema = False

    plan = planner_agent(query=query, cfg=cfg)
    LOG.info("Planner returned plan: %s", plan)

    data_cfg = cfg.get("data", {})
    df = load_data(data_cfg)
    LOG.info("Loaded data: %s rows", getattr(df, "shape", (0, 0))[0])

    results = {"query": query, "plan": plan, "schema": bool(schema), "rows": getattr(df, "shape", (0, 0))[0]}
    try:
        raw_hypos = _flexible_call(generate_hypotheses, df, group_col="campaign_name", lookback_days=cfg.get("lookback_days", 30))
        LOG.info("Generated raw hypotheses: %s", len(raw_hypos) if raw_hypos is not None else 0)

        evaluated = evaluate_hypotheses(df, raw_hypos or [])
        LOG.info("Evaluator returned %s items", len(evaluated))

        insights = insight_agent(df, evaluated)
        LOG.info("Insight returned: keys=%s", list(insights.keys()) if isinstance(insights, dict) else str(type(insights)))

        creatives = generate_creatives(df, n_per_campaign=3)
        LOG.info("Generated creatives: %s", len(creatives))
    except Exception as e:
        LOG.exception("generate_hypotheses error, fallback to []: %s", e)
        raw_hypos = []
        evaluated = []
        insights = {}
        creatives = []

    kpis = compute_kpis(df)
    results.update({
        "insights_count": len(insights) if isinstance(insights, dict) else 0,
        "evaluated_count": len(evaluated),
        "creatives_count": len(creatives),
        "kpis": kpis,
    })

    LOG.info("run_pipeline: finished summary: %s", results)
    return results
