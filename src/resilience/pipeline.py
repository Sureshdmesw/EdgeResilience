from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Optional

from src.ai.predictive_engine import PredictionResult
from src.resilience.connectivity import (
    ConnectivityObservation,
    evaluate_connectivity,
)
from src.resilience.evidence_buffer import EvidenceBuffer
from src.resilience.risk_state import (
    RiskState,
    derive_risk_state,
)


@dataclass(frozen=True)
class PipelineInput:
    """
    Inputs required by the EdgeResilience orchestration layer.

    PredictionResult contains the predictive AI output and its
    model metadata. ConnectivityObservation contains the current
    connectivity measurements. Integrity and sensor plausibility
    scores are deterministic supporting signals.
    """

    prediction: PredictionResult
    uncertainty_score: float
    connectivity: ConnectivityObservation
    integrity_score: float = 1.0
    sensor_plausibility_score: float = 1.0


@dataclass(frozen=True)
class PipelineOutput:
    """
    Deterministic output of one EdgeResilience evaluation cycle.

    This output represents risk interpretation and resilience
    state only. It does not issue vehicle commands or perform
    external CAN communication.
    """

    risk_state: RiskState
    connectivity_state: str
    local_inference_allowed: bool
    local_buffering_required: bool
    synchronization_allowed: bool
    evidence_required: bool
    reason_codes: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the pipeline result into JSON-friendly primitives.
        """

        result = asdict(self)

        result["risk_state"] = asdict(
            self.risk_state
        )

        result["reason_codes"] = list(
            self.reason_codes
        )

        return result


class EdgeResiliencePipeline:
    """
    EdgeResilience-native orchestration layer.

    Pipeline:

        Predictive AI
             |
             v
        Risk State
             |
             v
     Connectivity State
             |
             v
       Evidence Decision
             |
             v
       Evidence Buffer

    The pipeline provides local predictive intelligence and
    resilience-state interpretation.

    Safety boundary:
        - no vehicle actuation
        - no direct control commands
        - no external CAN transmission
        - no production vehicle connection
        - no physical vehicle validation
    """

    def __init__(
        self,
        evidence_buffer: Optional[EvidenceBuffer] = None,
    ) -> None:
        """
        Create the pipeline.

        If no evidence buffer is supplied, create a bounded local
        buffer with capacity for 128 records.
        """

        self.evidence_buffer = (
            evidence_buffer
            if evidence_buffer is not None
            else EvidenceBuffer(
                max_records=128
            )
        )

    def evaluate(
        self,
        pipeline_input: PipelineInput,
        *,
        event_id: Optional[str] = None,
    ) -> PipelineOutput:
        """
        Evaluate one EdgeResilience observation.

        The predictive result is converted into the mapping expected
        by the validated risk-state engine. Connectivity is evaluated
        independently and then combined with the risk state.

        Evidence is captured whenever the risk engine or connectivity
        engine determines that evidence is required.
        """

        prediction = pipeline_input.prediction

        # -----------------------------------------------------------------
        # 1. Convert the predictive result into the risk engine contract.
        # -----------------------------------------------------------------

        prediction_mapping: dict[str, Any] = {
            "y3_probability": (
                prediction.y3_probability
            ),
            "y6_probability": (
                prediction.y6_probability
            ),
            "y3_risk_level": (
                prediction.y3_risk_level
            ),
            "y6_risk_level": (
                prediction.y6_risk_level
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
        }

        # -----------------------------------------------------------------
        # 2. Derive deterministic cyber-physical resilience state.
        # -----------------------------------------------------------------

        risk_state = derive_risk_state(
            prediction_mapping,
            uncertainty_score=(
                pipeline_input.uncertainty_score
            ),
            packet_loss_rate=(
                pipeline_input
                .connectivity
                .packet_loss_rate
            ),
            latency_ms=(
                pipeline_input
                .connectivity
                .latency_ms
            ),
            heartbeat_failure=float(
                pipeline_input
                .connectivity
                .heartbeat_failure
            ),
            integrity_score=(
                pipeline_input.integrity_score
            ),
            sensor_plausibility_score=(
                pipeline_input
                .sensor_plausibility_score
            ),
        )

        # -----------------------------------------------------------------
        # 3. Evaluate connectivity independently.
        # -----------------------------------------------------------------

        connectivity_decision = evaluate_connectivity(
            pipeline_input.connectivity
        )

        # -----------------------------------------------------------------
        # 4. Decide whether local evidence capture is required.
        #
        # Evidence is required if:
        #   a) the risk engine explicitly requests it, OR
        #   b) connectivity requires local buffering.
        # -----------------------------------------------------------------

        evidence_required = (
            risk_state.evidence_required
            or connectivity_decision.local_buffering_required
        )

        if evidence_required:
            self._capture_evidence(
                pipeline_input=(
                    pipeline_input
                ),
                risk_state=risk_state,
                connectivity_decision=(
                    connectivity_decision
                ),
                event_id=event_id,
            )

        # -----------------------------------------------------------------
        # 5. Return the combined deterministic state.
        # -----------------------------------------------------------------

        return PipelineOutput(
            risk_state=risk_state,
            connectivity_state=(
                connectivity_decision
                .state
                .value
            ),
            local_inference_allowed=(
                connectivity_decision
                .local_inference_allowed
            ),
            local_buffering_required=(
                connectivity_decision
                .local_buffering_required
            ),
            synchronization_allowed=(
                connectivity_decision
                .synchronization_allowed
            ),
            evidence_required=evidence_required,
            reason_codes=(
                risk_state.reason_codes
            ),
        )

    def _capture_evidence(
        self,
        *,
        pipeline_input: PipelineInput,
        risk_state: RiskState,
        connectivity_decision: Any,
        event_id: Optional[str],
    ) -> None:
        """
        Capture one deterministic evidence record.

        EvidenceBuffer owns timestamp generation and SHA-256
        record hashing. This method only constructs the risk-state
        and telemetry payloads.

        No network transmission occurs here.
        """

        # -------------------------------------------------------------
        # Generate a deterministic event identifier when one is not
        # explicitly supplied by the caller.
        # -------------------------------------------------------------

        if event_id is None:
            from src.resilience.evidence_buffer import sha256_canonical

            event_fingerprint = sha256_canonical(
                {
                    "y3_probability": (
                        pipeline_input
                        .prediction
                        .y3_probability
                    ),
                    "y6_probability": (
                        pipeline_input
                        .prediction
                        .y6_probability
                    ),
                    "connectivity": (
                        connectivity_decision
                        .state
                        .value
                    ),
                }
            )

            event_id = f"edge:{event_fingerprint[:16]}"

        # -------------------------------------------------------------
        # Risk-state payload.
        # -------------------------------------------------------------

        risk_state_payload = asdict(
            risk_state
        )

        # -------------------------------------------------------------
        # Telemetry and model-provenance payload.
        # -------------------------------------------------------------

        telemetry_payload: dict[str, Any] = {
            "prediction": {
                "y3_probability": (
                    pipeline_input
                    .prediction
                    .y3_probability
                ),
                "y6_probability": (
                    pipeline_input
                    .prediction
                    .y6_probability
                ),
                "y3_risk_level": (
                    pipeline_input
                    .prediction
                    .y3_risk_level
                ),
                "y6_risk_level": (
                    pipeline_input
                    .prediction
                    .y6_risk_level
                ),
                "model_name": (
                    pipeline_input
                    .prediction
                    .model_name
                ),
                "model_source": (
                    pipeline_input
                    .prediction
                    .model_source
                ),
                "feature_count": (
                    pipeline_input
                    .prediction
                    .feature_count
                ),
                "observation_steps": (
                    pipeline_input
                    .prediction
                    .observation_steps
                ),
            },
            "connectivity": {
                "packet_loss_rate": (
                    pipeline_input
                    .connectivity
                    .packet_loss_rate
                ),
                "latency_ms": (
                    pipeline_input
                    .connectivity
                    .latency_ms
                ),
                "heartbeat_failure": (
                    pipeline_input
                    .connectivity
                    .heartbeat_failure
                ),
                "state": (
                    connectivity_decision
                    .state
                    .value
                ),
            },
            "uncertainty_score": (
                pipeline_input
                .uncertainty_score
            ),
            "integrity_score": (
                pipeline_input
                .integrity_score
            ),
            "sensor_plausibility_score": (
                pipeline_input
                .sensor_plausibility_score
            ),
        }

        # -------------------------------------------------------------
        # EvidenceBuffer owns canonicalization, timestamping, and
        # SHA-256 digest generation.
        # -------------------------------------------------------------

        self.evidence_buffer.append(
            event_id=event_id,
            risk_state=risk_state_payload,
            telemetry=telemetry_payload,
        )