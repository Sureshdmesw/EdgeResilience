import json
import hashlib
from pathlib import Path
import sys
import random

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.resilience.temporal_scenario_generator_v3 import (
    SEED,
    OBSERVATION_STEPS,
    FUTURE_HORIZON,
    generate_temporal_scenario,
)


SCENARIO_COUNT = 5000

OUTPUT_DIR = Path("data/processed/temporal")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DATASET_PATH = OUTPUT_DIR / "edgeresilience_temporal_dataset_v3.jsonl"
MANIFEST_PATH = OUTPUT_DIR / "edgeresilience_temporal_dataset_v3_manifest.json"


def sha256_file(path):
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def main():
    rng = random.Random(SEED)

    records = [
        generate_temporal_scenario(index, rng)
        for index in range(SCENARIO_COUNT)
    ]

    with DATASET_PATH.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(
                json.dumps(
                    record,
                    separators=(",", ":"),
                )
                + "\n"
            )

    feature_names = list(
        records[0]["observations"][0].keys()
    )

    regimes = {}

    for record in records:
        regime = record["regime"]
        regimes[regime] = regimes.get(regime, 0) + 1

    manifest = {
        "dataset_name":
            "EdgeResilience Temporal Dataset V3",

        "version":
            "v3",

        "purpose":
            "Synthetic temporal predictive-intelligence benchmark",

        "generator":
            "src/resilience/temporal_scenario_generator_v3.py",

        "seed":
            SEED,

        "record_count":
            len(records),

        "observation_steps":
            OBSERVATION_STEPS,

        "future_horizon":
            FUTURE_HORIZON,

        "features_per_observation":
            len(feature_names),

        "feature_names":
            feature_names,

        "latent_regime":
            {
                "present_in_generator": True,
                "exposed_as_model_feature": False,
                "purpose":
                    "Synthetic scenario-generation mechanism only",
            },

        "regime_distribution":
            regimes,

        "target":
            {
                "name":
                    "future_degradation",

                "definition":
                    "current_resilience - future_resilience",

                "clipped_to":
                    [0.0, 1.0],
            },

        "cyber_provenance":
            {
                "contract":
                    "10 HCRL-validated cyber feature names",

                "values_are_raw_hcrl_measurements":
                    False,

                "raw_hcrl_records_directly_used":
                    False,

                "description":
                    "Synthetic cyber values using the validated "
                    "EdgeResilience cyber feature contract.",
            },

        "vehicle_testing_boundary":
            {
                "physical_vehicle":
                    False,

                "external_can_transmission":
                    False,

                "direct_actuation":
                    False,

                "production_vehicle_connection":
                    False,
            },

        "snapdragon":
            {
                "hardware_verified":
                    False,

                "npu_verified":
                    False,

                "performance_measured":
                    False,
            },

        "provenance_classification":
            "new EdgeResilience synthetic artifact",

        "dataset_sha256":
            None,
    }

    MANIFEST_PATH.write_text(
        json.dumps(
            manifest,
            indent=2,
        ),
        encoding="utf-8",
    )

    dataset_hash = sha256_file(DATASET_PATH)

    manifest["dataset_sha256"] = dataset_hash

    MANIFEST_PATH.write_text(
        json.dumps(
            manifest,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("=" * 90)
    print("EDGERESILIENCE TEMPORAL DATASET V3")
    print("=" * 90)
    print(f"Records: {len(records)}")
    print(f"Observation steps: {OBSERVATION_STEPS}")
    print(f"Features per observation: {len(feature_names)}")
    print(f"Future horizon: {FUTURE_HORIZON}")
    print()
    print("Regime distribution:")

    for regime, count in sorted(regimes.items()):
        print(f"{regime:25s}: {count}")

    print()
    print(f"Dataset: {DATASET_PATH}")
    print(f"Manifest: {MANIFEST_PATH}")
    print(f"SHA256: {dataset_hash}")
    print()
    print("DATASET_V3_BUILD = PASS")


if __name__ == "__main__":
    main()
