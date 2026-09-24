import json
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

DATASET = Path(
    "data/processed/temporal/edgeresilience_temporal_dataset_v3.jsonl"
)

records = []

with DATASET.open("r", encoding="utf-8") as f:
    for line in f:
        records.append(json.loads(line))

# ---------------------------------------------------------------------
# Recover the exact feature contract from the dataset itself
# ---------------------------------------------------------------------

feature_names = list(records[0]["observations"][0].keys())

for record in records:
    for observation in record["observations"]:
        if list(observation.keys()) != feature_names:
            raise ValueError(
                "Feature ordering/schema mismatch detected."
            )

# ---------------------------------------------------------------------
# Convert observation dictionaries -> numeric tensor
# Shape: (samples, timesteps, features)
# ---------------------------------------------------------------------

X_seq = np.asarray(
    [
        [
            [observation[name] for name in feature_names]
            for observation in record["observations"]
        ]
        for record in records
    ],
    dtype=np.float32
)

y = np.asarray(
    [record["future_degradation"] for record in records],
    dtype=np.float32
)

n, steps, features = X_seq.shape

indices = np.arange(n)

train_idx, test_idx = train_test_split(
    indices,
    test_size=0.20,
    random_state=42
)

# ---------------------------------------------------------------------
# Evaluation helper
# ---------------------------------------------------------------------

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
        y[train_idx]
    )

    pred = model.predict(
        X[test_idx]
    )

    mae = mean_absolute_error(
        y[test_idx],
        pred
    )

    rmse = mean_squared_error(
        y[test_idx],
        pred
    ) ** 0.5

    print(
        f"{name:<30} "
        f"features={X.shape[1]:>3} "
        f"MAE={mae:.4f} "
        f"RMSE={rmse:.4f}"
    )

    return mae, rmse


# ---------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------

print("=" * 90)
print("EDGERESILIENCE V3 TEMPORAL INFORMATION BENCHMARK")
print("=" * 90)

print(f"Samples: {n}")
print(f"Observation steps: {steps}")
print(f"Features per step: {features}")
print(f"Total flattened features: {steps * features}")
print(f"Train: {len(train_idx)}")
print(f"Test: {len(test_idx)}")
print()

results = {}

# 1. Final timestep
X_final = X_seq[:, -1, :]

results["final"] = evaluate(
    "FINAL TIMESTEP",
    X_final
)

# 2. Mean over time
X_mean = X_seq.mean(axis=1)

results["mean"] = evaluate(
    "MEAN OVER TIME",
    X_mean
)

# 3. Full temporal sequence flattened
X_full = X_seq.reshape(
    n,
    steps * features
)

results["full"] = evaluate(
    "FULL 12-STEP",
    X_full
)

# ---------------------------------------------------------------------
# Mean target baseline
# ---------------------------------------------------------------------

baseline = np.full_like(
    y[test_idx],
    y[train_idx].mean()
)

baseline_mae = mean_absolute_error(
    y[test_idx],
    baseline
)

baseline_rmse = mean_squared_error(
    y[test_idx],
    baseline
) ** 0.5

print()
print("MEAN TARGET BASELINE")

print(
    f"{'MEAN BASELINE':<30} "
    f"features={0:>3} "
    f"MAE={baseline_mae:.4f} "
    f"RMSE={baseline_rmse:.4f}"
)

# ---------------------------------------------------------------------
# Temporal information analysis
# ---------------------------------------------------------------------

print()
print("TEMPORAL_INFORMATION_GAP")

full_vs_final_mae = (
    results["final"][0] -
    results["full"][0]
)

mean_vs_final_mae = (
    results["mean"][0] -
    results["final"][0]
)

print(
    f"Full vs final MAE delta: "
    f"{full_vs_final_mae:+.4f}"
)

print(
    f"Mean vs final MAE delta: "
    f"{mean_vs_final_mae:+.4f}"
)

if results["full"][0] + 1e-6 < results["final"][0]:
    print("TEMPORAL_SIGNAL = PRESENT")
else:
    print("TEMPORAL_SIGNAL = NOT_DEMONSTRATED")

print()
print("TEMPORAL_INFORMATION_BENCHMARK = PASS")
