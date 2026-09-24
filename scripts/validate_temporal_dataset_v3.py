import json
from pathlib import Path

DATASET = Path(
    "data/processed/temporal/edgeresilience_temporal_dataset_v3.jsonl"
)

records = [
    json.loads(line)
    for line in DATASET.read_text(encoding="utf-8").splitlines()
    if line.strip()
]

targets = [
    float(record["future_degradation"])
    for record in records
]

current = [
    float(record["current_resilience"])
    for record in records
]

future = [
    float(record["future_resilience"])
    for record in records
]

print("=" * 80)
print("EDGERESILIENCE V3 DATASET VALIDATION")
print("=" * 80)

print(f"Records: {len(records)}")
print(f"Observation steps: {len(records[0]['observations'])}")
print(f"Features per observation: {len(records[0]['observations'][0])}")

print(
    f"Current resilience: "
    f"min={min(current):.4f}, "
    f"max={max(current):.4f}, "
    f"mean={sum(current)/len(current):.4f}"
)

print(
    f"Future resilience: "
    f"min={min(future):.4f}, "
    f"max={max(future):.4f}, "
    f"mean={sum(future)/len(future):.4f}"
)

print(
    f"Future degradation: "
    f"min={min(targets):.4f}, "
    f"max={max(targets):.4f}, "
    f"mean={sum(targets)/len(targets):.4f}"
)

print(
    f"Zero degradation: "
    f"{sum(value == 0.0 for value in targets)}"
)

print(
    f"Meaningful degradation (>=0.05): "
    f"{sum(value >= 0.05 for value in targets)}"
)

assert len(records) == 5000
assert len(records[0]["observations"]) == 12
assert len(records[0]["observations"][0]) == 17
assert all(0.0 <= value <= 1.0 for value in targets)
assert all("regime" in record for record in records)

print()
print("DATASET_V3_VALIDATION = PASS")
