from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence

from src.ai.v4_inference import V4InferenceEngine, V4PredictionResult
from src.resilience.connectivity import (
    ConnectivityObservation,
    evaluate_connectivity,
    should_synchronize,
)
from src.resilience.evidence_buffer import EvidenceBuffer
from src.resilience.v4_risk import (
    V4RiskInterpretation,
    interpret_v4_degradation,
)


@dataclass(frozen=True)
class V4RuntimeResult:
    cycle_id: str
    prediction: V4PredictionResult
    risk: V4RiskInterpretation

    connectivity_state: str
    local_inference_allowed: bool
    local_buffering_required: bool
    synchronization_allowed: bool

    recovery_detected: bool
    synchronization_ready: bool
    evidence_count: int

    reason_codes: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class V4EdgeResilienceRuntime:
    """
    EdgeResilience-native runtime path.

    Pipeline:

        17 x 12 observations
            -> V4 temporal model
            -> future degradation
            -> V4 risk interpretation
            -> connectivity policy
            -> local evidence
            -> recovery/synchronization readiness

    Safety boundary:
        - software simulation only
        - no physical vehicle
        - no external CAN transmission
        - no direct actuation
        - no production vehicle connection
    """

    def __init__(
        self,
        *,
        checkpoint_path: str,
        evidence_buffer: EvidenceBuffer | None = None,
    ) -> None:
        self.engine = V4InferenceEngine(
            checkpoint_path
        )

        self.evidence_buffer = (
            evidence_buffer
            if evidence_buffer is not None
            else EvidenceBuffer(max_records=100)
        )

        self.previous_connectivity = None

    def evaluate_cycle(
        self,
        *,
        cycle_id: str,
        observations: Sequence[Mapping[str, Any]],
        connectivity: ConnectivityObservation,
    ) -> V4RuntimeResult:

        prediction = self.engine.predict(
            observations
        )

        risk = interpret_v4_degradation(
            prediction.predicted_future_degradation
        )

        connectivity_decision = evaluate_connectivity(
            connectivity
        )

        current_state = (
            connectivity_decision.state
        )

        recovery_detected = False

        if self.previous_connectivity is not None:
            recovery_detected = should_synchronize(
                self.previous_connectivity,
                current_state,
            )

        evidence_required = (
            risk.evidence_required
            or connectivity_decision.local_buffering_required
        )

        if evidence_required:
            self.evidence_buffer.append(
                event_id=f"v4:{cycle_id}",
                risk_state={
                    "future_degradation": (
                        prediction.predicted_future_degradation
                    ),
                    "predictive_risk_level": (
                        risk.predictive_risk_level
                    ),
                    "reason_codes": (
                        risk.reason_codes
                    ),
                    "policy_name": (
                        risk.policy_name
                    ),
                },
                telemetry={
                    "cycle_id": cycle_id,
                    "connectivity_state": (
                        current_state.value
                    ),
                    "packet_loss_rate": (
                        connectivity.packet_loss_rate
                    ),
                    "latency_ms": (
                        connectivity.latency_ms
                    ),
                    "heartbeat_failure": (
                        connectivity.heartbeat_failure
                    ),
                    "model_name": (
                        prediction.model_name
                    ),
                    "model_source": (
                        prediction.model_source
                    ),
                    "feature_count": (
                        prediction.feature_count
                    ),
                    "observation_steps": (
                        prediction.observation_steps
                    ),
                },
            )

        synchronization_ready = (
            recovery_detected
            and connectivity_decision.synchronization_allowed
        )

        reason_codes = tuple(
            list(risk.reason_codes)
            + [connectivity_decision.reason]
            + (
                ["CONNECTIVITY_RECOVERY_DETECTED"]
                if recovery_detected
                else []
            )
            + (
                ["SYNCHRONIZATION_READY"]
                if synchronization_ready
                else []
            )
        )

        self.previous_connectivity = current_state

        return V4RuntimeResult(
            cycle_id=cycle_id,
            prediction=prediction,
            risk=risk,
            connectivity_state=current_state.value,
            local_inference_allowed=(
                connectivity_decision.local_inference_allowed
            ),
            local_buffering_required=(
                connectivity_decision.local_buffering_required
            ),
            synchronization_allowed=(
                connectivity_decision.synchronization_allowed
            ),
            recovery_detected=recovery_detected,
            synchronization_ready=synchronization_ready,
            evidence_count=self.evidence_buffer.size,
            reason_codes=reason_codes,
        )
