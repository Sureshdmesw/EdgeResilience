import json
from pathlib import Path
import numpy as np

DATASET = Path(
    "data/processed/temporal/edgeresilience_temporal_dataset_v4.jsonl"
)

records = [
    json.loads(line)
    for line in DATASET.open(
        "r",
        encoding="utf-8",
    )
]

assert len(records) == 5000

steps = {
    len(r["observations"])
    for r in records
}

assert steps == {12}

feature_counts = {
    len(r["observations"][0])
    for r in records
}

assert feature_counts == {17}

targets = np.asarray(
    [
        r["future_degradation"]
        for r in records
    ],
    dtype=float,
)

current = np.asarray(
    [
        r["current_resilience"]
        for r in records
    ],
    dtype=float,
)

future = np.asarray(
    [
        r["future_resilience"]
        for r in records
    ],
    dtype=float,
)

assert np.all(targets >= 0.0)
assert np.all(targets <= 1.0)

meaningful = np.sum(
    targets >= 0.05
)

print("=" * 80)
print("EDGERESILIENCE V4 DATASET VALIDATION")
print("=" * 80)

print(f"Records: {len(records)}")
print(f"Observation steps: {sorted(steps)}")
print(f"Features per observation: {sorted(feature_counts)}")

print(
    f"Current resilience: "
    f"{current.min():.4f}-"
    f"{current.max():.4f}"
)

print(
    f"Future resilience: "
    f"{future.min():.4f}-"
    f"{future.max():.4f}"
)

print(
    f"Future degradation: "
    f"{targets.min():.4f}-"
    f"{targets.max():.4f}"
)

print(
    f"Mean future degradation: "
    f"{targets.mean():.4f}"
)

print(
    f"Zero degradation: "
    f"{np.sum(targets == 0.0)}"
)

print(
    f"Meaningful degradation >= 0.05: "
    f"{meaningful}"
)

print()
print("DATASET_V4_VALIDATION = PASS")
