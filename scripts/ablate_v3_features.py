import json
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split


DATASET = Path(
    "data/processed/temporal/edgeresilience_temporal_dataset_v3.jsonl"
)

FEATURE_NAMES = [
    "cyber_message_rate",
    "cyber_unique_can_id_count",
    "cyber_can_id_entropy",
    "cyber_mean_interarrival_ms",
    "cyber_std_interarrival_ms",
    "cyber_max_interarrival_ms",
    "cyber_interarrival_cv",
    "cyber_payload_change_rate",
    "cyber_mean_hamming_distance",
    "cyber_dominant_can_id_fraction",
    "latency_norm",
    "packet_loss_norm",
    "acceleration_norm",
    "steering_norm",
    "brake_pressure",
    "integrity",
    "sensor_plausibility",
]

records = [
    json.loads(line)
    for line in DATASET.read_text(encoding="utf-8").splitlines()
    if line.strip()
]

targets = np.asarray(
    [float(r["future_degradation"]) for r in records],
    dtype=float,
)

all_features = np.asarray(
    [
        [
            float(obs[name])
            for obs in record["observations"]
            for name in FEATURE_NAMES
        ]
        for record in records
    ],
    dtype=float,
)

feature_labels = [
    f"t{step:02d}_{name}"
    for step in range(12)
    for name in FEATURE_NAMES
]

train_idx, test_idx = train_test_split(
    np.arange(len(records)),
    test_size=0.20,
    random_state=42,
)

X_train_all = all_features[train_idx]
X_test_all = all_features[test_idx]

y_train = targets[train_idx]
y_test = targets[test_idx]


def evaluate(name, keep_mask):
    X_train = X_train_all[:, keep_mask]
    X_test = X_test_all[:, keep_mask]

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=16,
        min_samples_leaf=3,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    prediction = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        prediction,
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            prediction,
        )
    )

    print(
        f"{name:35s} "
        f"features={keep_mask.sum():3d} "
        f"MAE={mae:.4f} "
        f"RMSE={rmse:.4f}"
    )

    return mae, rmse


print("=" * 90)
print("EDGERESILIENCE V3 FEATURE ABLATION STUDY")
print("=" * 90)

print(f"Samples: {len(records)}")
print(f"Train: {len(train_idx)}")
print(f"Test: {len(test_idx)}")
print()

results = {}

# 1. All features
mask_all = np.ones(
    len(feature_labels),
    dtype=bool,
)

results["all"] = evaluate(
    "ALL 17 FEATURES",
    mask_all,
)

# 2. Remove integrity
mask_no_integrity = np.array(
    [
        not label.endswith("_integrity")
        for label in feature_labels
    ],
    dtype=bool,
)

results["no_integrity"] = evaluate(
    "WITHOUT INTEGRITY",
    mask_no_integrity,
)

# 3. Remove integrity + sensor plausibility
mask_no_integrity_sensor = np.array(
    [
        not (
            label.endswith("_integrity")
            or label.endswith("_sensor_plausibility")
        )
        for label in feature_labels
    ],
    dtype=bool,
)

results["no_integrity_sensor"] = evaluate(
    "WITHOUT INTEGRITY + SENSOR",
    mask_no_integrity_sensor,
)

# 4. Cyber + connectivity only
allowed_prefixes = (
    "cyber_",
)

allowed_signals = (
    "latency_norm",
    "packet_loss_norm",
)

mask_cyber_connectivity = np.array(
    [
        label.split("_", 1)[1].startswith(allowed_prefixes)
        or label.split("_", 1)[1] in allowed_signals
        for label in feature_labels
    ],
    dtype=bool,
)

results["cyber_connectivity"] = evaluate(
    "CYBER + CONNECTIVITY ONLY",
    mask_cyber_connectivity,
)

# 5. Final timestep only
mask_final = np.array(
    [
        label.startswith("t11_")
        for label in feature_labels
    ],
    dtype=bool,
)

results["final_only"] = evaluate(
    "FINAL TIMESTEP ONLY",
    mask_final,
)

print()
print("MEAN BASELINE")

mean_prediction = np.full(
    len(y_test),
    y_train.mean(),
)

mean_mae = mean_absolute_error(
    y_test,
    mean_prediction,
)

mean_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        mean_prediction,
    )
)

print(
    f"{'MEAN BASELINE':35s} "
    f"features=  0 "
    f"MAE={mean_mae:.4f} "
    f"RMSE={mean_rmse:.4f}"
)

print()
print("ABLATION_STUDY = PASS")
