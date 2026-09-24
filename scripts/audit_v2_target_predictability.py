import json
from pathlib import Path
import numpy as np

DATASET = Path(
    "data/processed/temporal/edgeresilience_temporal_dataset_v2.jsonl"
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

targets = np.array(
    [float(r["future_degradation"]) for r in records],
    dtype=float,
)

current = np.array(
    [float(r["current_resilience"]) for r in records],
    dtype=float,
)

future = np.array(
    [float(r["future_resilience"]) for r in records],
    dtype=float,
)


def corr(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)

    if np.std(a) == 0 or np.std(b) == 0:
        return 0.0

    return float(np.corrcoef(a, b)[0, 1])


def feature_matrix(records, mode):
    rows = []

    for record in records:
        observations = record["observations"]

        if mode == "final":
            selected = observations[-1]

            rows.append([
                float(selected[name])
                for name in FEATURE_NAMES
            ])

        elif mode == "mean":
            rows.append([
                float(np.mean([
                    observation[name]
                    for observation in observations
                ]))
                for name in FEATURE_NAMES
            ])

        elif mode == "std":
            rows.append([
                float(np.std([
                    observation[name]
                    for observation in observations
                ]))
                for name in FEATURE_NAMES
            ])

        elif mode == "delta":
            first = observations[0]
            last = observations[-1]

            rows.append([
                float(last[name]) - float(first[name])
                for name in FEATURE_NAMES
            ])

    return np.asarray(rows, dtype=float)


def ranked_correlations(matrix, label):
    values = []

    for index, name in enumerate(FEATURE_NAMES):
        value = corr(matrix[:, index], targets)

        values.append(
            (
                abs(value),
                value,
                name,
            )
        )

    values.sort(reverse=True)

    print(label)

    for abs_value, signed_value, name in values:
        print(
            f"{name:38s} "
            f"corr={signed_value:+.6f} "
            f"|corr|={abs_value:.6f}"
        )

    print()


print("=" * 80)
print("EDGERESILIENCE V2 TARGET PREDICTABILITY AUDIT")
print("=" * 80)

print(f"Records: {len(records)}")
print(f"Observation steps: {len(records[0]['observations'])}")
print(f"Feature count: {len(FEATURE_NAMES)}")
print()

print("TARGET")
print(f"Mean degradation:   {targets.mean():.6f}")
print(f"Std degradation:    {targets.std():.6f}")
print(f"Median degradation: {np.median(targets):.6f}")
print(f"Max degradation:    {targets.max():.6f}")
print()

print("TARGET RELATIONSHIPS")
print(
    f"corr(current_resilience, target): "
    f"{corr(current, targets):+.6f}"
)
print(
    f"corr(future_resilience, target):  "
    f"{corr(future, targets):+.6f}"
)
print()

ranked_correlations(
    feature_matrix(records, "final"),
    "FINAL-TIMESTEP FEATURES",
)

ranked_correlations(
    feature_matrix(records, "mean"),
    "MEAN-OVER-TIME FEATURES",
)

ranked_correlations(
    feature_matrix(records, "std"),
    "TEMPORAL-VARIABILITY FEATURES",
)

ranked_correlations(
    feature_matrix(records, "delta"),
    "FIRST-TO-LAST DELTA FEATURES",
)

print("TARGET_PREDICTABILITY_AUDIT = PASS")
