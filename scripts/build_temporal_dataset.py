from pathlib import Path
import sys
import json
import hashlib

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.resilience.temporal_scenario_generator import (
    SEED,
    OBSERVATION_STEPS,
    FUTURE_HORIZON,
    generate_temporal_scenario,
)


OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "temporal"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

DATASET_PATH = (
    OUTPUT_DIR
    / "edgeresilience_temporal_dataset.jsonl"
)

MANIFEST_PATH = (
    OUTPUT_DIR
    / "edgeresilience_temporal_dataset_manifest.json"
)

SCENARIO_COUNT = 5000


def sha256_file(path):
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def flatten_scenario(scenario):

    return {
        "scenario_id":
            scenario["scenario_id"],

        "observations":
            scenario["observations"],

        "current_resilience":
            float(
                scenario["current_resilience"]
            ),

        "future_resilience":
            float(
                scenario["future_resilience"]
            ),

        "future_degradation":
            float(
                scenario["future_degradation"]
            ),
    }


def main():

    rng = __import__("random").Random(SEED)

    with DATASET_PATH.open(
        "w",
        encoding="utf-8",
    ) as output:

        for index in range(
            SCENARIO_COUNT
        ):

            scenario = generate_temporal_scenario(
                index,
                rng,
            )

            record = flatten_scenario(
                scenario
            )

            output.write(
                json.dumps(
                    record,
                    separators=(",", ":"),
                )
                + "\n"
            )

    manifest = {
        "dataset_name":
            "EdgeResilience Temporal Dataset",

        "dataset_status":
            "generated",

        "scenario_count":
            SCENARIO_COUNT,

        "observation_steps":
            OBSERVATION_STEPS,

        "future_horizon":
            FUTURE_HORIZON,

        "seed":
            SEED,

        "feature_sources": [
            "synthetic vehicle state",
            "synthetic connectivity state",
            "EdgeResilience cyber-state representation",
        ],

        "target": {
            "name":
                "future_degradation",
            "definition":
                "current resilience minus separately evolved future resilience",
        },

        "label_used_as_feature":
            False,

        "physical_vehicle_test":
            False,

        "external_can_transmission":
            False,

        "direct_actuation":
            False,

        "snapdragon_hardware_verified":
            False,
    }

    with MANIFEST_PATH.open(
        "w",
        encoding="utf-8",
    ) as handle:

        json.dump(
            manifest,
            handle,
            indent=2,
        )

    checksum = sha256_file(
        DATASET_PATH
    )

    print("=" * 90)
    print(
        "EDGERESILIENCE TEMPORAL DATASET BUILD"
    )
    print("=" * 90)
    print(
        f"Scenarios: {SCENARIO_COUNT}"
    )
    print(
        f"Observation steps: {OBSERVATION_STEPS}"
    )
    print(
        f"Future horizon: {FUTURE_HORIZON}"
    )
    print(
        f"Dataset: {DATASET_PATH}"
    )
    print(
        f"Manifest: {MANIFEST_PATH}"
    )
    print(
        f"SHA256: {checksum}"
    )
    print()
    print(
        "DATASET_BUILD = PASS"
    )


if __name__ == "__main__":
    main()
