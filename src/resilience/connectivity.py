from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Mapping


class ConnectivityState(str, Enum):
    CONNECTED = "CONNECTED"
    DEGRADED = "DEGRADED"
    DISCONNECTED = "DISCONNECTED"


@dataclass(frozen=True)
class ConnectivityObservation:
    packet_loss_rate: float
    latency_ms: float
    heartbeat_failure: bool


@dataclass(frozen=True)
class ConnectivityDecision:
    state: ConnectivityState
    local_inference_allowed: bool
    local_buffering_required: bool
    synchronization_allowed: bool
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def clamp(
    value: float,
    low: float = 0.0,
    high: float = 1.0,
) -> float:
    return max(
        low,
        min(high, float(value)),
    )


def classify_connectivity(
    observation: ConnectivityObservation,
) -> ConnectivityState:
    packet_loss = clamp(
        observation.packet_loss_rate
    )

    latency = max(
        0.0,
        float(observation.latency_ms),
    )

    if (
        observation.heartbeat_failure
        or packet_loss >= 0.80
    ):
        return ConnectivityState.DISCONNECTED

    if (
        packet_loss >= 0.20
        or latency >= 250.0
    ):
        return ConnectivityState.DEGRADED

    return ConnectivityState.CONNECTED


def evaluate_connectivity(
    observation: ConnectivityObservation,
) -> ConnectivityDecision:
    state = classify_connectivity(
        observation
    )

    if state == ConnectivityState.CONNECTED:
        return ConnectivityDecision(
            state=state,
            local_inference_allowed=True,
            local_buffering_required=False,
            synchronization_allowed=True,
            reason="CONNECTIVITY_NOMINAL",
        )

    if state == ConnectivityState.DEGRADED:
        return ConnectivityDecision(
            state=state,
            local_inference_allowed=True,
            local_buffering_required=True,
            synchronization_allowed=False,
            reason="CONNECTIVITY_DEGRADED_LOCAL_CONTINUITY",
        )

    return ConnectivityDecision(
        state=state,
        local_inference_allowed=True,
        local_buffering_required=True,
        synchronization_allowed=False,
        reason="CONNECTIVITY_LOSS_LOCAL_CONTINUITY",
    )


def should_synchronize(
    previous_state: ConnectivityState,
    current_state: ConnectivityState,
) -> bool:
    """
    Return True when connectivity has recovered from a
    degraded/disconnected state.

    This is a software synchronization policy only.
    It performs no network transmission.
    """

    return (
        current_state == ConnectivityState.CONNECTED
        and previous_state
        in {
            ConnectivityState.DEGRADED,
            ConnectivityState.DISCONNECTED,
        }
    )


def build_observation(
    values: Mapping[str, Any],
) -> ConnectivityObservation:
    return ConnectivityObservation(
        packet_loss_rate=float(
            values.get(
                "packet_loss_rate",
                0.0,
            )
        ),
        latency_ms=float(
            values.get(
                "latency_ms",
                0.0,
            )
        ),
        heartbeat_failure=bool(
            values.get(
                "heartbeat_failure",
                False,
            )
        ),
    )
