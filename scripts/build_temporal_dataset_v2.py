import json
import hashlib
from pathlib import Path
import random
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.resilience.temporal_scenario_generator_conditioned_v2 import (
    SEED,
    OBSERVATION_STEPS,
    FUTURE_HORIZON,
    generate_temporal_scenario,
)

SCENARIO_COUNT = 5000

OUTPUT_DIR = Path("data/processed/temporal")

DATASET_PATH = OUTPUT_DIR / "edgeresilience_temporal_dataset_v2.jsonl"
MANIFEST_PATH = OUTPUT_DIR / "edgeresilience_temporal_dataset_v2_manifest.json"


def sha256_file(path):
    digest = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def main():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    rng = random.Random(SEED)

    with DATASET_PATH.open("w", encoding="utf-8") as f:

        for index in range(SCENARIO_COUNT):

            scenario = generate_temporal_scenario(
                index,
                rng,
            )

            f.write(
                json.dumps(
                    scenario,
                    separators=(",", ":"),
                )
                + "\n"
            )

    dataset_sha256 = sha256_file(DATASET_PATH)

    manifest = {
        "dataset_name":
            "EdgeResilience Conditioned Temporal Predictive Dataset",

        "dataset_version":
            "v2_conditioned_synthetic",

        "record_count":
            SCENARIO_COUNT,

        "observation_steps":
            OBSERVATION_STEPS,

        "future_horizon":
            FUTURE_HORIZON,

        "features_per_observation":
            17,

        "cyber_features":
            [
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
            ],

        "connectivity_features":
            [
                "latency_norm",
                "packet_loss_norm",
            ],

        "vehicle_features":
            [
                "acceleration_norm",
                "steering_norm",
                "brake_pressure",
            ],

        "additional_features":
            [
                "integrity",
                "sensor_plausibility",
            ],

        "feature_provenance":
            "Synthetic temporal scenarios using the validated EdgeResilience 10-feature HCRL cyber-state contract. Feature values in this dataset are synthetically generated and are NOT raw HCRL measurements.",

        "target":
            "future_degradation",

        "target_definition":
            "Current resilience minus separately evolved future resilience, clipped to [0,1].",

        "future_event_generation":
            "Future stress-event probability is conditioned partly on the observed cyber, connectivity, vehicle, and integrity state. The future state is still separately evolved and stochastic.",

        "target_leakage":
            "Future state variables are not included in the observation sequence.",

        "seed":
            SEED,

        "label_used_as_feature":
            False,

        "raw_hcrl_records_directly_used":
            False,

        "physical_vehicle_test":
            False,

        "external_can_transmission":
            False,

        "direct_actuation":
            False,

        "snapdragon_hardware_verified":
            False,

        "dataset_sha256":
            dataset_sha256,

        "generator":
            "src/resilience/temporal_scenario_generator_conditioned_v2.py",

        "evidence_status":
            "new_edge_resilience_synthetic_dataset",
    }

    MANIFEST_PATH.write_text(
        json.dumps(
            manifest,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("=" * 80)
    print("EDGERESILIENCE CONDITIONED TEMPORAL DATASET V2")
    print("=" * 80)

    print(f"Records: {SCENARIO_COUNT}")
    print(f"Observation steps: {OBSERVATION_STEPS}")
    print("Features per observation: 17")
    print(f"Future horizon: {FUTURE_HORIZON}")
    print(f"Dataset: {DATASET_PATH}")
    print(f"Manifest: {MANIFEST_PATH}")
    print(f"SHA256: {dataset_sha256}")

    print()
    print("DATASET_BUILD_V2 = PASS")


if __name__ == "__main__":
    main()
