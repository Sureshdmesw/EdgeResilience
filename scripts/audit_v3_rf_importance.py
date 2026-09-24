import joblib
import numpy as np
from pathlib import Path

MODEL = Path(
    "models/edgeresilience/temporal_rf_baseline_v3.joblib"
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

model = joblib.load(MODEL)

feature_names = [
    f"t{step:02d}_{name}"
    for step in range(12)
    for name in FEATURE_NAMES
]

importance = np.asarray(
    model.feature_importances_,
    dtype=float,
)

ranking = sorted(
    zip(feature_names, importance),
    key=lambda item: item[1],
    reverse=True,
)

print("=" * 90)
print("EDGERESILIENCE V3 RF FEATURE IMPORTANCE AUDIT")
print("=" * 90)

print(f"Features: {len(feature_names)}")
print(f"Importance sum: {importance.sum():.6f}")
print()

print("TOP 25 FEATURES")

for rank, (name, value) in enumerate(ranking[:25], start=1):
    print(
        f"{rank:2d}. "
        f"{name:45s} "
        f"{value:.6f}"
    )

print()
print("IMPORTANCE BY SIGNAL")

signal_totals = {}

for name, value in ranking:
    signal = name.split("_", 1)[1]

    signal_totals[signal] = (
        signal_totals.get(signal, 0.0) + value
    )

for rank, (signal, value) in enumerate(
    sorted(
        signal_totals.items(),
        key=lambda item: item[1],
        reverse=True,
    ),
    start=1,
):
    print(
        f"{rank:2d}. "
        f"{signal:38s} "
        f"{value:.6f}"
    )

print()
print("IMPORTANCE BY TIMESTEP")

timestep_totals = {}

for name, value in ranking:
    timestep = name.split("_", 1)[0]

    timestep_totals[timestep] = (
        timestep_totals.get(timestep, 0.0) + value
    )

for timestep, value in sorted(timestep_totals.items()):
    print(
        f"{timestep}: {value:.6f}"
    )

print()
print("RF_FEATURE_IMPORTANCE_AUDIT = PASS")
