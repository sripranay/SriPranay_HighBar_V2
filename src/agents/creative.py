# src/agents.creative.py
from __future__ import annotations
import logging
from typing import Any, Dict, List
import pandas as pd

LOG = logging.getLogger(__name__)


def generate_creatives(df: pd.DataFrame, n_per_campaign: int = 2) -> List[Dict[str, Any]]:
    if df is None or df.empty:
        LOG.info("generate_creatives() called with empty input, returning empty list")
        return []
    if "campaign_name" not in df.columns:
        LOG.info("generate_creatives(): campaign_name not in df")
        return []
    campaigns = pd.Series(df["campaign_name"].unique()).tolist()
    creatives = []
    for c in campaigns[:10]:
        for i in range(min(n_per_campaign, 3)):
            creatives.append({"campaign": c, "creative_id": f"{c}_rec_{i}", "text": f"Try variant {i} for {c}"})
    LOG.info("generate_creatives() generated %d creatives", len(creatives))
    return creatives
