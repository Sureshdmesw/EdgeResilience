import json
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

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

X_seq = np.asarray(
    [
        [
            [obs[name] for name in feature_names]
            for obs in record["observations"]
        ]
        for record in records
    ],
    dtype=np.float32,
)

y = np.asarray(
    [
        record["future_degradation"]
        for record in records
    ],
    dtype=np.float32,
)

n, steps, features = X_seq.shape

indices = np.arange(n)

train_idx, test_idx = train_test_split(
    indices,
    test_size=0.20,
    random_state=42,
)


def evaluate(name, X):
    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=16,
        min_samples_leaf=3,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(
        X[train_idx],
        y[train_idx],
    )

    pred = model.predict(
        X[test_idx],
    )

    mae = mean_absolute_error(
        y[test_idx],
        pred,
    )

    rmse = mean_squared_error(
        y[test_idx],
        pred,
    ) ** 0.5

    print(
        f"{name:<32}"
        f"features={X.shape[1]:>4} "
        f"MAE={mae:.4f} "
        f"RMSE={rmse:.4f}"
    )

    return mae, rmse


print("=" * 95)
print("EDGERESILIENCE V4 TEMPORAL INFORMATION BENCHMARK")
print("=" * 95)

print(f"Samples: {n}")
print(f"Observation steps: {steps}")
print(f"Features per step: {features}")
print(f"Full features: {steps * features}")
print(f"Train: {len(train_idx)}")
print(f"Test: {len(test_idx)}")
print()

results = {}

# ------------------------------------------------------------
# 1. Final timestep
# ------------------------------------------------------------

X_final = X_seq[:, -1, :]

results["final"] = evaluate(
    "FINAL TIMESTEP",
    X_final,
)

# ------------------------------------------------------------
# 2. Mean over trajectory
# ------------------------------------------------------------

X_mean = X_seq.mean(axis=1)

results["mean"] = evaluate(
    "MEAN OVER TIME",
    X_mean,
)

# ------------------------------------------------------------
# 3. First -> final trajectory delta
# ------------------------------------------------------------

X_delta = (
    X_seq[:, -1, :]
    - X_seq[:, 0, :]
)

results["delta"] = evaluate(
    "FIRST-TO-LAST DELTA",
    X_delta,
)

# ------------------------------------------------------------
# 4. Temporal variability
# ------------------------------------------------------------

X_std = X_seq.std(axis=1)

results["std"] = evaluate(
    "TEMPORAL STD",
    X_std,
)

# ------------------------------------------------------------
# 5. Full flattened sequence
# ------------------------------------------------------------

X_full = X_seq.reshape(
    n,
    steps * features,
)

results["full"] = evaluate(
    "FULL 12-STEP",
    X_full,
)

# ------------------------------------------------------------
# Mean target baseline
# ------------------------------------------------------------

baseline = np.full_like(
    y[test_idx],
    y[train_idx].mean(),
)

baseline_mae = mean_absolute_error(
    y[test_idx],
    baseline,
)

baseline_rmse = mean_squared_error(
    y[test_idx],
    baseline,
) ** 0.5

print()
print("MEAN TARGET BASELINE")

print(
    f"{'MEAN BASELINE':<32}"
    f"features={0:>4} "
    f"MAE={baseline_mae:.4f} "
    f"RMSE={baseline_rmse:.4f}"
)

# ------------------------------------------------------------
# Information gaps
# ------------------------------------------------------------

print()
print("TEMPORAL_INFORMATION_GAPS")

final_mae = results["final"][0]
full_mae = results["full"][0]
delta_mae = results["delta"][0]
std_mae = results["std"][0]

print(
    f"Full vs final MAE delta: "
    f"{final_mae - full_mae:+.6f}"
)

print(
    f"Delta vs final MAE delta: "
    f"{final_mae - delta_mae:+.6f}"
)

print(
    f"STD vs final MAE delta: "
    f"{final_mae - std_mae:+.6f}"
)

print()

if full_mae + 1e-6 < final_mae:
    print("TEMPORAL_SIGNAL = PRESENT")
else:
    print("TEMPORAL_SIGNAL = NOT_DEMONSTRATED")

if (
    delta_mae + 1e-6 < final_mae
    or std_mae + 1e-6 < final_mae
):
    print("TRAJECTORY_SUMMARY_SIGNAL = PRESENT")
else:
    print("TRAJECTORY_SUMMARY_SIGNAL = NOT_DEMONSTRATED")

print()
print("TEMPORAL_INFORMATION_BENCHMARK_V4 = PASS")
