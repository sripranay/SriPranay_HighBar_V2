import argparse
import yaml
from src.orchestrator import run_pipeline


def load_config(path="config/config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="Run Kasparro FB Agentic V2")
    parser.add_argument("query", nargs="?", default="Analyze ROAS drop")
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    cfg = load_config(args.config)
    result = run_pipeline(args.query, cfg)
    print("=== RUN SUMMARY ===")
    print(result)

if __name__ == "__main__":
    main()
