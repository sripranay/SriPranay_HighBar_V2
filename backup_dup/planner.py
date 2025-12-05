from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

def planner_agent(user_query: str, cfg: Dict[str, Any]) -> List[str]:
    logger.info("planner_agent received query: %s", user_query)
    plan: List[str] = [
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
    # If config requests fast mode, shorten plan
    fast_mode = cfg.get("analysis", {}).get("fast_mode", False)
    if fast_mode:
        logger.info("planner_agent: fast_mode enabled, shortening plan")
        return ["load_data", "compute_kpis", "detect_roas_changes", "compile_report"]
    return plan
