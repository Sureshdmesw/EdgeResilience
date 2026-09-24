import json
from pathlib import Path

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split


DATASET = Path(
    "data/processed/temporal/edgeresilience_temporal_dataset.jsonl"
)

SEED = 42


def main():

    records = [
        json.loads(line)
        for line in DATASET.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    # Last observed cyber/connectivity/vehicle state.
    # This is a diagnostic baseline, not a trained model.
    X = np.array(
        [
            list(record["observations"][-1].values())
            for record in records
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

    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=SEED,
    )

    # Use current resilience as a reference predictor.
    current = np.array(
        [
            record["current_resilience"]
            for record in records
        ],
        dtype=np.float32,
    )

    _, current_test, _, _ = train_test_split(
        current,
        y,
        test_size=0.20,
        random_state=SEED,
    )

    # Simple persistence-style transformation:
    # lower current resilience -> larger expected degradation.
    prediction = 1.0 - current_test

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

    print("=" * 80)
    print("EDGERESILIENCE CURRENT-STATE DIAGNOSTIC")
    print("=" * 80)

    print(
        f"Test samples: {len(y_test)}"
    )

    print(
        f"Current-state diagnostic MAE:  {mae:.4f}"
    )

    print(
        f"Current-state diagnostic RMSE: {rmse:.4f}"
    )

    print()
    print(
        "This is a diagnostic only."
    )

    print(
        "It is NOT a trained predictive model."
    )

    print()
    print(
        "CURRENT_STATE_DIAGNOSTIC = PASS"
    )


if __name__ == "__main__":
    main()
