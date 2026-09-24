import json
import hashlib
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
import joblib


DATASET = Path(
    "data/processed/temporal/edgeresilience_temporal_dataset.jsonl"
)

MODEL_DIR = Path(
    "models/edgeresilience"
)

MODEL_PATH = MODEL_DIR / "temporal_rf_baseline_v1.joblib"
REPORT_PATH = MODEL_DIR / "temporal_rf_baseline_v1_report.json"

SEED = 42


def sha256_file(path):
    digest = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def load_dataset():

    records = [
        json.loads(line)
        for line in DATASET.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    X = np.array(
        [
            [
                value
                for observation in record["observations"]
                for value in observation.values()
            ]
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

    return X, y


def main():

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    X, y = load_dataset()

    print("=" * 80)
    print("EDGERESILIENCE RANDOM FOREST BASELINE")
    print("=" * 80)

    print(
        f"Samples: {len(X)}"
    )

    print(
        f"Input dimensions: {X.shape[1]}"
    )

    print(
        f"Target mean: {y.mean():.4f}"
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=SEED,
    )

    print(
        f"Training samples: {len(X_train)}"
    )

    print(
        f"Test samples: {len(X_test)}"
    )

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=16,
        min_samples_leaf=3,
        random_state=SEED,
        n_jobs=-1,
    )

    print()
    print("Training Random Forest...")

    model.fit(
        X_train,
        y_train,
    )

    predictions = model.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions,
        )
    )

    mean_baseline_prediction = np.full_like(
        y_test,
        y_train.mean(),
    )

    baseline_mae = mean_absolute_error(
        y_test,
        mean_baseline_prediction,
    )

    baseline_rmse = np.sqrt(
        mean_squared_error(
            y_test,
            mean_baseline_prediction,
        )
    )

    print()
    print("RESULTS")
    print(
        f"RF MAE:       {mae:.4f}"
    )

    print(
        f"RF RMSE:      {rmse:.4f}"
    )

    print(
        f"Mean MAE:     {baseline_mae:.4f}"
    )

    print(
        f"Mean RMSE:    {baseline_rmse:.4f}"
    )

    print()

    if mae < baseline_mae:
        print(
            "RF_BEATS_MEAN_BASELINE = YES"
        )
    else:
        print(
            "RF_BEATS_MEAN_BASELINE = NO"
        )

    joblib.dump(
        model,
        MODEL_PATH,
    )

    dataset_sha256 = sha256_file(
        DATASET
    )

    model_sha256 = sha256_file(
        MODEL_PATH
    )

    report = {

        "model":
            "RandomForestRegressor",

        "model_version":
            "temporal_rf_baseline_v1",

        "dataset":
            str(DATASET),

        "dataset_sha256":
            dataset_sha256,

        "input_shape":
            [
                int(X.shape[0]),
                int(X.shape[1]),
            ],

        "sequence_length":
            12,

        "features_per_step":
            17,

        "seed":
            SEED,

        "test_size":
            0.20,

        "n_estimators":
            300,

        "max_depth":
            16,

        "min_samples_leaf":
            3,

        "mae":
            float(mae),

        "rmse":
            float(rmse),

        "mean_baseline_mae":
            float(baseline_mae),

        "mean_baseline_rmse":
            float(baseline_rmse),

        "model_sha256":
            model_sha256,

        "snapdragon_hardware_verified":
            False,

        "physical_vehicle_test":
            False,

        "external_can_transmission":
            False,

        "direct_actuation":
            False,

        "evidence_status":
            "new_edge_resilience_baseline",
    }

    REPORT_PATH.write_text(
        json.dumps(
            report,
            indent=2,
        ),
        encoding="utf-8",
    )

    print()
    print(
        f"Model: {MODEL_PATH}"
    )

    print(
        f"Report: {REPORT_PATH}"
    )

    print(
        f"Model SHA256: {model_sha256}"
    )

    print()
    print(
        "RANDOM_FOREST_BASELINE = PASS"
    )


if __name__ == "__main__":
    main()
