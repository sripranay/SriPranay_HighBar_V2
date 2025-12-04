import yaml
from pathlib import Path
from .utils.loader import load_data
from .utils.schema_check import load_schema, check_schema
from .utils.logger import setup_logger
from .agents.insight import generate_hypotheses
from .agents.evaluator import evaluate_hypotheses
from .agents.creative import generate_creatives
import json

ROOT = Path(__file__).resolve().parents[1]

def save_json(obj, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def run_pipeline(user_query: str, cfg: dict):
    logger = setup_logger(level=cfg.get("logging", {}).get("level","INFO"),
                          logs_dir=cfg.get("logging", {}).get("logs_dir","logs"))
    logger.info("Starting pipeline")
    dp = Path(cfg["data"]["dataset_path"])
    sample = cfg["data"].get("sample", False)
    sample_n = cfg["data"].get("sample_n", 500)
    df = load_data(dp, sample=sample, sample_n=sample_n)
    logger.info(f"Loaded data: {len(df)} rows")
    # schema
    schema = load_schema(Path("schemas/schema_v1.json"))
    ok, msg = check_schema(df, schema)
    if not ok:
        logger.warning(f"Schema check failed: {msg}")
    else:
        logger.info(f"Schema check OK: {msg}")
    # insights
    lookback = cfg.get("analysis", {}).get("lookback_days", 14)
    hypos = generate_hypotheses(df, group_col="campaign_name", lookback_days=lookback)
    out_dir = Path(cfg.get("outputs", {}).get("reports_dir","reports"))
    save_json(hypos, out_dir / "insight_result_raw.json")
    logger.info(f"Saved raw hypotheses to {out_dir/'insight_result_raw.json'}")
    # evaluate
    thresholds = cfg.get("thresholds", {})
    evaluated = evaluate_hypotheses(hypos, thresholds)
    save_json(evaluated, out_dir / "insights.json")
    logger.info(f"Saved evaluated insights to {out_dir/'insights.json'}")
    # creatives
    creatives = generate_creatives(df, n_per_campaign=3)
    save_json(creatives, out_dir / "creatives.json")
    logger.info(f"Saved creatives to {out_dir/'creatives.json'}")
    # human report (simple markdown)
    md_lines = ["# Facebook Ads Agentic Analysis Report", "", f"Generated: AUTO", "", "## Quick summary", ""]
    md_lines.append(f"Validated insights: {sum(1 for i in evaluated if i.get('validated'))} / {len(evaluated)}")
    md_lines.append("")
    md_lines.append("## Validated Insights (Full)")
    for i in evaluated:
        md_lines.append(f"### {i.get('hypothesis')}")
        md_lines.append(f"- Evidence: {i.get('evidence')}")
        md_lines.append(f"- Confidence: {i.get('confidence')}")
        md_lines.append(f"- Validated: {i.get('validated')}")
        md_lines.append("")
    md_lines.append("## Creative Recommendations")
    for idx, c in enumerate(creatives[:50], start=1):
        md_lines.append(f"{idx}. {c.get('headline')} — {c.get('body')} — {c.get('cta')}")
    (out_dir).mkdir(parents=True, exist_ok=True)
    with open(out_dir / "report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    logger.info(f"Saved final report to {out_dir/'report.md'}")
    summary = {"validated_count": sum(1 for i in evaluated if i.get("validated")), "creatives_for": list({c["campaign_name"] for c in creatives})}
    return summary
