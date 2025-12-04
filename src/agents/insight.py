from typing import List, Dict, Any
import pandas as pd
from datetime import timedelta
from collections import defaultdict
from ..utils.helpers import safe_pct_change

def generate_hypotheses(df: pd.DataFrame, group_col="campaign_name", lookback_days=14) -> List[Dict[str,Any]]:
    # Compare recent window vs previous same-length window
    out = []
    if "date_parsed" not in df.columns:
        return out
    df = df.dropna(subset=["date_parsed"]).copy()
    latest = df["date_parsed"].max()
    recent_start = latest - pd.Timedelta(days=lookback_days-1)
    prev_start = recent_start - pd.Timedelta(days=lookback_days)
    recent = df[(df["date_parsed"] >= recent_start) & (df["date_parsed"] <= latest)]
    prev = df[(df["date_parsed"] >= prev_start) & (df["date_parsed"] < recent_start)]
    groups = set(list(recent[group_col].unique()) + list(prev[group_col].unique()))
    for g in groups:
        r = recent[recent[group_col] == g]
        p = prev[prev[group_col] == g]
        if len(r) < 1 or len(p) < 1:
            continue
        metrics = {}
        for metric in ["ctr","spend","impressions","purchases","roas"]:
            rv = r[metric].mean() if metric in r.columns else None
            pv = p[metric].mean() if metric in p.columns else None
            pct = safe_pct_change(rv, pv) if rv is not None and pv is not None else None
            metrics[metric] = {"recent": rv, "previous": pv, "pct_change": pct}
        # simple rule-based mapping to hypothesis
        # if CTR fell significantly
        ctr_pct = metrics.get("ctr", {}).get("pct_change")
        if ctr_pct is not None and ctr_pct < -5:
            out.append({
                "hypothesis": f"CTR fell - creatives may be fatigued for {g}.",
                "segment": g,
                "evidence": {"ctr": metrics["ctr"]},
                "raw_metrics": metrics,
                "validated": False
            })
        # if purchases dropped
        purchases_pct = metrics.get("purchases", {}).get("pct_change")
        if purchases_pct is not None and purchases_pct < -5:
            out.append({
                "hypothesis": f"Purchases dropped — conversion / creative performance may be weaker for {g}.",
                "segment": g,
                "evidence": {"purchases": metrics["purchases"]},
                "raw_metrics": metrics,
                "validated": False
            })
    return out
