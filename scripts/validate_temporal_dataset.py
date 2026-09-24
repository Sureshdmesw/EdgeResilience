import json
from pathlib import Path

DATASET = Path("data/processed/temporal/edgeresilience_temporal_dataset.jsonl")
EXPECTED_RECORDS = 5000
EXPECTED_STEPS = 12

def main():
    if not DATASET.exists():
        print(f"ERROR: Dataset not found: {DATASET}")
        raise SystemExit(1)

    records = []
    with DATASET.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    print(f"Records: {len(records)}")

    if len(records) != EXPECTED_RECORDS:
        print(f"ERROR: Expected {EXPECTED_RECORDS} records")
        raise SystemExit(1)

    ids = [r["scenario_id"] for r in records]
    if len(set(ids)) != len(ids):
        print("ERROR: Duplicate scenario IDs")
        raise SystemExit(1)

    step_counts = [len(r["observations"]) for r in records]
    if any(x != EXPECTED_STEPS for x in step_counts):
        print("ERROR: Incorrect observation-step count")
        raise SystemExit(1)

    current = [float(r["current_resilience"]) for r in records]
    future = [float(r["future_resilience"]) for r in records]
    degradation = [float(r["future_degradation"]) for r in records]

    for name, values in [
        ("current_resilience", current),
        ("future_resilience", future),
        ("future_degradation", degradation),
    ]:
        if any(x < 0 or x > 1 for x in values):
            print(f"ERROR: {name} contains values outside [0, 1]")
            raise SystemExit(1)

    print(f"Current resilience: min={min(current):.4f}, max={max(current):.4f}, mean={sum(current)/len(current):.4f}")
    print(f"Future resilience: min={min(future):.4f}, max={max(future):.4f}, mean={sum(future)/len(future):.4f}")
    print(f"Future degradation: min={min(degradation):.4f}, max={max(degradation):.4f}, mean={sum(degradation)/len(degradation):.4f}")
    print(f"Zero degradation: {sum(x == 0 for x in degradation)}")
    print(f"Meaningful degradation (>=0.05): {sum(x >= 0.05 for x in degradation)}")

    print("DATASET_VALIDATION = PASS")

if __name__ == "__main__":
    main()
