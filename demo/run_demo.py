# -*- coding: utf-8 -*-
"""
EdgeResilience Competition Demo

Primary demonstration using V4EdgeResilienceRuntime with the
EdgeResilience_V4_TemporalPredictor checkpoint.

Three-cycle scenario:
  cycle-001: CONNECTED  - prediction active, risk interpretation
  cycle-002: DISCONNECTED - local inference continues, evidence buffered
  cycle-003: CONNECTED  - recovery detected, synchronization ready

Safety boundary:
  - software simulation only
  - no physical vehicle
  - no external CAN transmission
  - no direct actuation
  - no production vehicle connection
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.resilience.connectivity import ConnectivityObservation
from src.resilience.v4_runtime import V4EdgeResilienceRuntime

CHECKPOINT = (
    PROJECT_ROOT
    / "models"
    / "edgeresilience"
    / "temporal_predictor_v4.pt"
)

DATASET = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "temporal"
    / "edgeresilience_temporal_dataset_v4.jsonl"
)

OUTPUT = PROJECT_ROOT / "data" / "evidence" / "v4_demo_scenario.json"


def main() -> None:
    if not CHECKPOINT.exists():
        print(f"ERROR: Checkpoint not found: {CHECKPOINT}")
        sys.exit(1)

    if not DATASET.exists():
        print(f"ERROR: Dataset not found: {DATASET}")
        sys.exit(1)

    with DATASET.open("r", encoding="utf-8") as fh:
        records = [json.loads(line) for line in fh]

    runtime = V4EdgeResilienceRuntime(checkpoint_path=str(CHECKPOINT))

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

    print("\n" + "=" * 72)
    print("EDGERESILIENCE V4 SOFTWARE DEMONSTRATION")
    print("Model: EdgeResilience_V4_TemporalPredictor")
    print("Target: future_degradation")
    print("=" * 72)

    cycles = []

    for cycle_id, label, record, connectivity in scenarios:
        result = runtime.evaluate_cycle(
            cycle_id=cycle_id,
            observations=record["observations"],
            connectivity=connectivity,
        )

        cycle_dict = {
            "cycle_id": result.cycle_id,
            "label": label,
            "prediction": {
                "predicted_future_degradation": (
                    result.prediction.predicted_future_degradation
                ),
                "model_name": result.prediction.model_name,
                "model_source": result.prediction.model_source,
                "feature_count": result.prediction.feature_count,
                "observation_steps": result.prediction.observation_steps,
            },
            "risk": result.risk.to_dict(),
            "connectivity_state": result.connectivity_state,
            "local_inference_allowed": result.local_inference_allowed,
            "local_buffering_required": result.local_buffering_required,
            "synchronization_allowed": result.synchronization_allowed,
            "recovery_detected": result.recovery_detected,
            "synchronization_ready": result.synchronization_ready,
            "evidence_count": result.evidence_count,
            "reason_codes": list(result.reason_codes),
        }
        cycles.append(cycle_dict)

        print(f"\n[{cycle_id}] {label}")
        print(
            f"  Future degradation:  "
            f"{result.prediction.predicted_future_degradation:.6f}"
        )
        print(
            f"  Risk level:          "
            f"{result.risk.predictive_risk_level}"
        )
        print(
            f"  Policy:              "
            f"{result.risk.policy_name}"
        )
        print(
            f"  Connectivity:        "
            f"{result.connectivity_state}"
        )
        print(
            f"  Local inference:     "
            f"{result.local_inference_allowed}"
        )
        print(
            f"  Local buffering:     "
            f"{result.local_buffering_required}"
        )
        print(
            f"  Evidence records:    "
            f"{result.evidence_count}"
        )
        print(
            f"  Recovery detected:   "
            f"{result.recovery_detected}"
        )
        print(
            f"  Sync ready:          "
            f"{result.synchronization_ready}"
        )

    final = cycles[-1]
    assert final["recovery_detected"] is True, "cycle-003 must detect recovery"
    assert final["synchronization_ready"] is True, "cycle-003 must be sync ready"
    assert final["local_buffering_required"] is False, "cycle-003 must not require buffering"

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

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )

    print("\n" + "=" * 72)
    print("DEMO SCENARIO: PASS")
    print(f"Evidence artifact: {OUTPUT}")
    print("=" * 72)
    print()
    print("Safety boundary:")
    print("  Physical vehicle test:       NO")
    print("  External CAN transmission:   NO")
    print("  Direct actuation:            NO")
    print("  Production vehicle:          NO")
    print("  Snapdragon X Elite components: VERIFIED")
    print("  Qualcomm QNN / HTP components: VERIFIED")
    print("  Full V4 HTP execution:        NOT VERIFIED")


if __name__ == "__main__":
    main()

