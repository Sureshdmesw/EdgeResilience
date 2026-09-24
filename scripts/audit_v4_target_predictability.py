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

feature_names = list(
    records[0]["observations"][0].keys()
)

X = np.asarray(
    [
        [
            [
                obs[name]
                for name in feature_names
            ]
            for obs in r["observations"]
        ]
        for r in records
    ],
    dtype=float,
)

y = np.asarray(
    [
        r["future_degradation"]
        for r in records
    ],
    dtype=float,
)

final = X[:, -1, :]
mean = X.mean(axis=1)
delta = X[:, -1, :] - X[:, 0, :]
variability = X.std(axis=1)

def corr(a, b):
    if np.std(a) < 1e-12:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])

print("=" * 90)
print("EDGERESILIENCE V4 TARGET PREDICTABILITY AUDIT")
print("=" * 90)

print(
    f"Target mean: {y.mean():.6f}"
)

print(
    f"Target std: {y.std():.6f}"
)

print(
    f"Target median: {np.median(y):.6f}"
)

print(
    f"Target max: {y.max():.6f}"
)

print()
print("FINAL-TIMESTEP CORRELATIONS")

final_corr = []

for i, name in enumerate(feature_names):
    value = corr(
        final[:, i],
        y,
    )

    final_corr.append(
        (abs(value), value, name)
    )

for _, value, name in sorted(
    final_corr,
    reverse=True,
)[:17]:

    print(
        f"{name:<40} "
        f"{value:+.6f}"
    )

print()
print("TRAJECTORY DELTA CORRELATIONS")

delta_corr = []

for i, name in enumerate(feature_names):
    value = corr(
        delta[:, i],
        y,
    )

    delta_corr.append(
        (abs(value), value, name)
    )

for _, value, name in sorted(
    delta_corr,
    reverse=True,
)[:17]:

    print(
        f"{name:<40} "
        f"{value:+.6f}"
    )

print()
print("TEMPORAL VARIABILITY CORRELATIONS")

var_corr = []

for i, name in enumerate(feature_names):
    value = corr(
        variability[:, i],
        y,
    )

    var_corr.append(
        (abs(value), value, name)
    )

for _, value, name in sorted(
    var_corr,
    reverse=True,
)[:17]:

    print(
        f"{name:<40} "
        f"{value:+.6f}"
    )

max_delta = max(
    abs(x[1])
    for x in delta_corr
)

max_variability = max(
    abs(x[1])
    for x in var_corr
)

print()
print(
    f"Maximum absolute delta correlation: "
    f"{max_delta:.6f}"
)

print(
    f"Maximum absolute variability correlation: "
    f"{max_variability:.6f}"
)

print()
print("V4_TARGET_PREDICTABILITY_AUDIT = PASS")
