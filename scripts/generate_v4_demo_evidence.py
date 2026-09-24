from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.resilience.connectivity import ConnectivityObservation
from src.resilience.v4_runtime import V4EdgeResilienceRuntime


DATASET = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "temporal"
    / "edgeresilience_temporal_dataset_v4.jsonl"
)

CHECKPOINT = (
    PROJECT_ROOT
    / "models"
    / "edgeresilience"
    / "temporal_predictor_v4.pt"
)

OUTPUT = (
    PROJECT_ROOT
    / "data"
    / "evidence"
    / "v4_demo_scenario.json"
)


with DATASET.open("r", encoding="utf-8") as handle:
    records = [
        json.loads(line)
        for line in handle
    ]


runtime = V4EdgeResilienceRuntime(
    checkpoint_path=str(CHECKPOINT)
)


scenarios = [
    (
        "cycle-001",
        "Predictive warning / connected",
        records[0],
        ConnectivityObservation(
            packet_loss_rate=0.01,
            latency_ms=40.0,
            heartbeat_failure=False,
        ),
    ),
    (
        "cycle-002",
        "Connectivity loss / local resilience",
        records[1],
        ConnectivityObservation(
            packet_loss_rate=0.85,
            latency_ms=400.0,
            heartbeat_failure=True,
        ),
    ),
    (
        "cycle-003",
        "Connectivity recovery / synchronization",
        records[2],
        ConnectivityObservation(
            packet_loss_rate=0.01,
            latency_ms=40.0,
            heartbeat_failure=False,
        ),
    ),
]


cycles = []

for cycle_id, label, record, connectivity in scenarios:

    result = runtime.evaluate_cycle(
        cycle_id=cycle_id,
        observations=record["observations"],
        connectivity=connectivity,
    )

    cycles.append(
        {
            "cycle_id": result.cycle_id,
            "label": label,
            "prediction": result.prediction.__dict__,
            "risk": result.risk.to_dict(),
            "connectivity_state": result.connectivity_state,
            "local_inference_allowed": (
                result.local_inference_allowed
            ),
            "local_buffering_required": (
                result.local_buffering_required
            ),
            "synchronization_allowed": (
                result.synchronization_allowed
            ),
            "recovery_detected": (
                result.recovery_detected
            ),
            "synchronization_ready": (
                result.synchronization_ready
            ),
            "evidence_count": (
                result.evidence_count
            ),
            "reason_codes": list(
                result.reason_codes
            ),
        }
    )


payload = {
    "project": "EdgeResilience",
    "artifact": "V4 model-backed software demonstration",
    "model": {
        "name": "EdgeResilience_V4_TemporalPredictor",
        "checkpoint": str(CHECKPOINT),
        "feature_count": 17,
        "observation_steps": 12,
        "target": "future_degradation",
    },
    "policy": {
        "name": "V4_DEGRADATION_DEMO_POLICY_V1",
        "type": "deterministic interpretation",
        "learned_thresholds": False,
        "vehicle_safety_limits": False,
        "snapdragon_hardware_limits": False,
    },
    "safety_boundary": {
        "test_type": "software_simulation",
        "physical_vehicle": False,
        "external_can_transmission": False,
        "direct_actuation": False,
        "production_vehicle_connection": False,
    },
    "cycles": cycles,
}


OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

OUTPUT.write_text(
    json.dumps(
        payload,
        indent=2,
    ),
    encoding="utf-8",
)

print("=" * 72)
print("V4 DASHBOARD EVIDENCE GENERATED")
print("=" * 72)
print(f"Output: {OUTPUT}")
print(f"Cycles: {len(cycles)}")
print(
    f"Latest risk: "
    f"{cycles[-1]['risk']['predictive_risk_level']}"
)
print(
    f"Latest connectivity: "
    f"{cycles[-1]['connectivity_state']}"
)
print(
    f"Synchronization ready: "
    f"{cycles[-1]['synchronization_ready']}"
)
print()
print("V4 DASHBOARD EVIDENCE: PASS")
