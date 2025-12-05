from typing import List, Dict, Any
import random

def generate_creatives_for_segment(segment_name: str, sample_msg: str=None, n=3) -> List[Dict[str,str]]:
    out = []
    sample_msg = (sample_msg or "").strip()
    for i in range(1, n+1):
        headline = f"{segment_name} – Try our new fit #{i}"
        body = (sample_msg + " ").strip() + "Now available. Limited time offer."
        cta = "Shop Now"
        out.append({"campaign_name": segment_name, "headline": headline, "body": body, "cta": cta})
    return out

def generate_creatives(df, n_per_campaign=3):
    out = []
    if "campaign_name" in df.columns:
        for name, g in df.groupby("campaign_name"):
            sample_msg = g["creative_message"].dropna().iloc[0] if "creative_message" in g.columns and len(g["creative_message"].dropna())>0 else ""
            out.extend(generate_creatives_for_segment(name, sample_msg=sample_msg, n=n_per_campaign))
    else:
        out.extend(generate_creatives_for_segment("all", sample_msg="", n=n_per_campaign))
    return out
