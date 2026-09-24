import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.resilience.temporal_scenario_generator_v4 import (
    FEATURE_NAMES,
    OBSERVATION_STEPS,
    FUTURE_HORIZON,
    SEED,
    generate_dataset,
)

COUNT = 5000

OUT_DIR = ROOT / "data" / "processed" / "temporal"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DATASET_PATH = (
    OUT_DIR /
    "edgeresilience_temporal_dataset_v4.jsonl"
)

MANIFEST_PATH = (
    OUT_DIR /
    "edgeresilience_temporal_dataset_v4_manifest.json"
)

records = generate_dataset(
    count=COUNT,
    seed=SEED,
)

with DATASET_PATH.open(
    "w",
    encoding="utf-8",
) as f:

    for record in records:
        f.write(
            json.dumps(
                record,
                sort_keys=True,
            )
            + "\n"
        )

sha256 = hashlib.sha256()

with DATASET_PATH.open("rb") as f:
    for chunk in iter(
        lambda: f.read(1024 * 1024),
        b"",
    ):
        sha256.update(chunk)

manifest = {
    "artifact": "EdgeResilience V4 temporal synthetic benchmark",
    "dataset_path": str(
        DATASET_PATH.relative_to(ROOT)
    ),
    "records": COUNT,
    "observation_steps": OBSERVATION_STEPS,
    "future_horizon": FUTURE_HORIZON,
    "features_per_observation": len(FEATURE_NAMES),
    "feature_names": FEATURE_NAMES,
    "seed": SEED,
    "target": "future_degradation",
    "target_definition": (
        "current_resilience - separately generated "
        "future_resilience"
    ),
    "latent_regime_present": True,
    "latent_regime_used_as_model_feature": False,
    "latent_trajectory_memory_used": True,
    "raw_hcrl_records_used": False,
    "cyber_values_are_raw_hcrl_measurements": False,
    "cyber_feature_contract": (
        "10 validated HCRL-derived feature names; "
        "synthetic values"
    ),
    "physical_vehicle_test": False,
    "external_can_transmission": False,
    "direct_actuation": False,
    "production_vehicle_connection": False,
    "snapdragon_hardware_verified": False,
    "provenance_classification": (
        "new EdgeResilience synthetic artifact"
    ),
    "sha256": sha256.hexdigest(),
}

with MANIFEST_PATH.open(
    "w",
    encoding="utf-8",
) as f:
    json.dump(
        manifest,
        f,
        indent=2,
    )

print("=" * 80)
print("EDGERESILIENCE V4 DATASET BUILD")
print("=" * 80)
print(f"Records: {COUNT}")
print(f"Steps: {OBSERVATION_STEPS}")
print(f"Features: {len(FEATURE_NAMES)}")
print(f"Dataset: {DATASET_PATH}")
print(f"SHA256: {sha256.hexdigest()}")
print()
print("DATASET_V4_BUILD = PASS")
