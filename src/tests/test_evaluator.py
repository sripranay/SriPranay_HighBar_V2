from src.agents.evaluator import evaluate_hypotheses

def test_evaluate_simple():
    hypos = [
        {"hypothesis": "test", "segment": "A", "raw_metrics": {"ctr": {"pct_change": -30}} , "evidence": {}}
    ]
    out = evaluate_hypotheses(hypos, {"min_samples": 10})
    assert isinstance(out, list)
    assert out[0]["confidence"] >= 0
