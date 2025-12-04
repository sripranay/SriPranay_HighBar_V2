import numpy as np
import math

def safe_pct_change(new, old):
    try:
        if old is None or old == 0 or math.isnan(old):
            return None
        return 100.0 * (new - old) / old
    except Exception:
        return None

def compute_confidence(pct_change, n_samples=10):
    # simple heuristic: more change + more data -> more confidence
    if pct_change is None:
        return 0.0
    base = min(abs(pct_change) / 100.0, 1.0)
    conf = base * (1 - 0.5 / (1 + n_samples/10))
    return float(max(0.0, min(conf, 1.0)))
