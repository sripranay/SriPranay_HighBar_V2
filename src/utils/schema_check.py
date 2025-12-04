import json
from pathlib import Path

def load_schema(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def check_schema(df, schema: dict):
    required = schema.get("required_columns", [])
    missing = [c for c in required if c not in df.columns]
    ok = len(missing) == 0
    msg = {"ok": ok, "missing": missing}
    return ok, msg
