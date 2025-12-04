from typing import List, Dict, Any
from ..utils.helpers import compute_confidence
import numpy as np

def evaluate_hypotheses(hypotheses: List[Dict[str,Any]], thresholds: Dict[str, float]) -> List[Dict[str,Any]]:
    out = []
    for h in hypotheses:
        evidence = h.get("evidence", {})
        raw = h.get("raw_metrics", {})
        # Compute confidence from pct change of main metric and sample size heuristic
        # Pick main metric
        main = None
        if "ctr" in evidence:
            main = "ctr"
        elif "purchases" in evidence:
            main = "purchases"
        else:
            # fallback choose first key
            main = next(iter(evidence.keys()))
        m = raw.get(main, {})
        pct = m.get("pct_change")
        # n_samples: crude approximation - use 10 as default
        n = thresholds.get("min_samples", 10)
        confidence = compute_confidence(pct, n)
        impact = "low"
        if pct is None:
            impact = "unknown"
        elif abs(pct) > 50:
            impact = "high"
        elif abs(pct) > 15:
            impact = "medium"
        out_h = {
            "hypothesis": h.get("hypothesis"),
            "segment": h.get("segment"),
            "evidence": m,
            "impact": impact,
            "confidence": float(round(confidence, 3)),
            "validated": confidence >= 0.15
        }
        out.append(out_h)
    return out
