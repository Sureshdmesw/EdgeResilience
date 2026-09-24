import json
from pathlib import Path

DATASET = Path(
    "data/processed/temporal/edgeresilience_temporal_dataset_v2.jsonl"
)

EXPECTED_RECORDS = 5000
EXPECTED_STEPS = 12
EXPECTED_FEATURES = 17


def main():

    if not DATASET.exists():
        print(f"ERROR: Dataset not found: {DATASET}")
        raise SystemExit(1)

    records = [
        json.loads(line)
        for line in DATASET.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    print(f"Records: {len(records)}")

    if len(records) != EXPECTED_RECORDS:
        print(
            f"ERROR: Expected {EXPECTED_RECORDS} records"
        )
        raise SystemExit(1)

    ids = [
        record["scenario_id"]
        for record in records
    ]

    if len(set(ids)) != len(ids):
        print("ERROR: Duplicate scenario IDs")
        raise SystemExit(1)

    step_counts = [
        len(record["observations"])
        for record in records
    ]

    if any(
        count != EXPECTED_STEPS
        for count in step_counts
    ):
        print("ERROR: Incorrect observation-step count")
        raise SystemExit(1)

    feature_counts = [
        len(record["observations"][0])
        for record in records
    ]

    if any(
        count != EXPECTED_FEATURES
        for count in feature_counts
    ):
        print("ERROR: Incorrect feature count")
        raise SystemExit(1)

    current = np_values(
        records,
        "current_resilience",
    )

    future = np_values(
        records,
        "future_resilience",
    )

    degradation = np_values(
        records,
        "future_degradation",
    )

    for name, values in [
        ("current_resilience", current),
        ("future_resilience", future),
        ("future_degradation", degradation),
    ]:

        if any(
            value < 0.0 or value > 1.0
            for value in values
        ):
            print(
                f"ERROR: {name} outside [0,1]"
            )
            raise SystemExit(1)

    print(
        f"Current resilience: "
        f"min={min(current):.4f}, "
        f"max={max(current):.4f}, "
        f"mean={mean(current):.4f}"
    )

    print(
        f"Future resilience: "
        f"min={min(future):.4f}, "
        f"max={max(future):.4f}, "
        f"mean={mean(future):.4f}"
    )

    print(
        f"Future degradation: "
        f"min={min(degradation):.4f}, "
        f"max={max(degradation):.4f}, "
        f"mean={mean(degradation):.4f}"
    )

    print(
        "Zero degradation:",
        sum(
            value == 0.0
            for value in degradation
        ),
    )

    print(
        "Meaningful degradation (>=0.05):",
        sum(
            value >= 0.05
            for value in degradation
        ),
    )

    print()
    print("DATASET_V2_VALIDATION = PASS")


def np_values(records, key):
    return [
        float(record[key])
        for record in records
    ]


def mean(values):
    return sum(values) / len(values)


if __name__ == "__main__":
    main()
