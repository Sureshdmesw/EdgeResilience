import json
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split


DATASET = Path(
    "data/processed/temporal/edgeresilience_temporal_dataset.jsonl"
)

SEED = 42


FEATURES = [
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


def main():

    records = [
        json.loads(line)
        for line in DATASET.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    # Use only the final observed timestep for this diagnostic.
    X = np.array(
        [
            [
                observation[feature]
                for feature in FEATURES
            ]
            for observation in (
                record["observations"][-1]
                for record in records
            )
        ],
        dtype=np.float32,
    )

    y = np.array(
        [
            record["future_degradation"]
            for record in records
        ],
        dtype=np.float32,
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=SEED,
    )

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=12,
        min_samples_leaf=5,
        random_state=SEED,
        n_jobs=-1,
    )

    model.fit(
        X_train,
        y_train,
    )

    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    print("=" * 80)
    print("EDGERESILIENCE FEATURE SIGNAL DIAGNOSTIC")
    print("=" * 80)

    print(
        f"Test MAE: {mae:.4f}"
    )

    print()
    print("FEATURE IMPORTANCE")

    ranking = sorted(
        zip(
            FEATURES,
            model.feature_importances_,
        ),
        key=lambda x: x[1],
        reverse=True,
    )

    for name, importance in ranking:
        print(
            f"{name:40s} {importance:.6f}"
        )

    print()
    print(
        "FEATURE_SIGNAL_DIAGNOSTIC = PASS"
    )


if __name__ == "__main__":
    main()
