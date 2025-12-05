from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)

def insight_agent(df: Any, cfg: Dict[str, Any]) -> Dict[str, Any]:
    """
    Minimal insight_agent stub used by orchestrator.
    Returns a minimal structure so pipeline runs.
    """
    logger.info("insight_agent called (stub)")
    return {"insights": [], "meta": {"rows": getattr(df, "shape", None)}}
