from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Optional

from src.ai.predictive_engine import PredictionResult
from src.resilience.connectivity import (
    ConnectivityObservation,
    ConnectivityState,
)
from src.resilience.pipeline import (
    EdgeResiliencePipeline,
    PipelineInput,
    PipelineOutput,
)
from src.resilience.synchronization import (
    RecoveryDecision,
    SynchronizationRecord,
    evaluate_recovery,
    prepare_synchronization_batch,
    validate_synchronization_batch,
)


@dataclass(frozen=True)
class ScenarioCycleResult:
    """
    Complete result for one EdgeResilience runtime cycle.

    This is a software/virtual-laboratory orchestration artifact.
    It does not transmit data, actuate a vehicle, or connect to
    an external CAN bus.
    """

    cycle_id: str
    pipeline: PipelineOutput
    recovery: RecoveryDecision
    synchronization_ready: bool
    synchronization_batch: tuple[SynchronizationRecord, ...]
    evidence_count: int

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)

        result["pipeline"] = self.pipeline.to_dict()
        result["recovery"] = self.recovery.to_dict()
        result["synchronization_batch"] = [
            asdict(record)
            for record in self.synchronization_batch
        ]

        return result


class EdgeResilienceScenarioRuntime:
    """
    Stateful orchestration layer for an EdgeResilience scenario.

    Lifecycle:

        prediction
            |
            v
        pipeline evaluation
            |
            v
        connectivity state tracking
            |
            v
        recovery detection
            |
            v
        synchronization manifest preparation

    Safety boundary:
        - no vehicle actuation
        - no direct control commands
        - no external CAN transmission
        - no production vehicle connection
        - no physical vehicle validation
        - synchronization is manifest preparation only
    """

    def __init__(
        self,
        pipeline: Optional[EdgeResiliencePipeline] = None,
    ) -> None:
        self.pipeline = (
            pipeline
            if pipeline is not None
            else EdgeResiliencePipeline()
        )

        self._previous_connectivity_state: Optional[
            ConnectivityState
        ] = None

    @property
    def previous_connectivity_state(
        self,
    ) -> Optional[ConnectivityState]:
        return self._previous_connectivity_state

    def evaluate_cycle(
        self,
        *,
        cycle_id: str,
        prediction: PredictionResult,
        uncertainty_score: float,
        connectivity: ConnectivityObservation,
        integrity_score: float = 1.0,
        sensor_plausibility_score: float = 1.0,
        event_id: Optional[str] = None,
    ) -> ScenarioCycleResult:
        """
        Evaluate one stateful EdgeResilience cycle.
        """

        pipeline_input = PipelineInput(
            prediction=prediction,
            uncertainty_score=uncertainty_score,
            connectivity=connectivity,
            integrity_score=integrity_score,
            sensor_plausibility_score=sensor_plausibility_score,
        )

        if event_id is None:
            event_id = f"edge:{cycle_id}"

        pipeline_output = self.pipeline.evaluate(
            pipeline_input,
            event_id=event_id,
        )

        current_state = ConnectivityState(
            pipeline_output.connectivity_state
        )

        previous_state = self._previous_connectivity_state

        if previous_state is None:
            recovery = RecoveryDecision(
                recovered=False,
                synchronization_allowed=False,
                records_available=self.pipeline.evidence_buffer.size,
                reason="INITIAL_CONNECTIVITY_STATE",
            )
        else:
            buffered_records = self.pipeline.evidence_buffer.snapshot(
                include_all=True
            )

            recovery = evaluate_recovery(
                previous_state,
                current_state,
                buffered_records,
            )

        synchronization_batch: list[
            SynchronizationRecord
        ] = []

        if recovery.recovered and recovery.synchronization_allowed:
            buffered_records = self.pipeline.evidence_buffer.snapshot(
                include_all=True
            )

            synchronization_batch = prepare_synchronization_batch(
                buffered_records
            )

        synchronization_ready = (
            bool(synchronization_batch)
            and validate_synchronization_batch(
                synchronization_batch
            )
        )

        self._previous_connectivity_state = current_state

        return ScenarioCycleResult(
            cycle_id=cycle_id,
            pipeline=pipeline_output,
            recovery=recovery,
            synchronization_ready=synchronization_ready,
            synchronization_batch=tuple(
                synchronization_batch
            ),
            evidence_count=self.pipeline.evidence_buffer.size,
        )
