import json
from eval.run_eval import run_full_eval

results = run_full_eval(3)

print(f"\nTotal results: {len(results)}")
for r in results:
    print("\n---")
    print("Test case:", r.get("test_case"))
    print("Response:", r.get("response"))
    print("Passed:", r.get("passed"))
    print("Reason:", r.get("reason"))
    print("DeepEval score:", r.get("deepeval_score"))
    print("DeepEval reason:", r.get("deepeval_reason"))

# Sanity checks
assert len(results) == 3, "Expected 3 results"
for r in results:
    assert set(r.keys()) >= {"test_case", "response", "passed", "reason", "deepeval_score", "deepeval_reason"}, f"Missing fields in {r}"
    assert not str(r.get("response", "")).startswith("Error:"), f"Target agent failed: {r}"
    assert not str(r.get("reason", "")).startswith("Error:"), f"Scorer agent failed: {r}"

with open("results/eval_results.json") as f:
    saved = json.load(f)
assert saved == results, "Saved file doesn't match returned results"

print("\n✅ Phase 4 test passed — full eval loop works end-to-end with DeepEval fields present.")