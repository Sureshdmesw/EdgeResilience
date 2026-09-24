from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


RISK_LEVELS = (
    "NORMAL",
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
)

CONFIDENCE_LEVELS = (
    "UNKNOWN",
    "LOW",
    "MEDIUM",
    "HIGH",
)

CONNECTIVITY_STATES = (
    "CONNECTED",
    "DEGRADED",
    "DISCONNECTED",
)


@dataclass(frozen=True)
class RiskState:
    """
    Deterministic interpretation of predictive and
    cyber-physical observations.

    This object contains state information only.
    It does not issue vehicle-control commands.
    """

    y3_probability: float
    y6_probability: float
    predictive_risk_level: str

    uncertainty_score: float
    confidence_level: str

    connectivity_state: str
    integrity_score: float
    sensor_plausibility_score: float

    resilience_score: float
    evidence_required: bool

    reason_codes: tuple[str, ...]

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


def probability_to_level(
    probability: float,
) -> str:
    probability = clamp(
        probability,
        0.0,
        1.0,
    )

    if probability < 0.05:
        return "NORMAL"

    if probability < 0.20:
        return "LOW"

    if probability < 0.50:
        return "MEDIUM"

    if probability < 0.80:
        return "HIGH"

    return "CRITICAL"


def uncertainty_to_confidence(
    uncertainty_score: float,
) -> str:
    """
    Interpret normalized uncertainty.

    Higher uncertainty means lower confidence.
    """

    uncertainty_score = clamp(
        uncertainty_score,
        0.0,
        1.0,
    )

    if uncertainty_score >= 0.75:
        return "LOW"

    if uncertainty_score >= 0.40:
        return "MEDIUM"

    if uncertainty_score >= 0.0:
        return "HIGH"

    return "UNKNOWN"


def connectivity_state(
    *,
    packet_loss_rate: float = 0.0,
    latency_ms: float = 0.0,
    heartbeat_failure: float = 0.0,
) -> str:
    """
    Deterministic connectivity classification.

    These thresholds are EdgeResilience policy defaults,
    not measured Snapdragon or vehicle limits.
    """

    packet_loss_rate = clamp(
        packet_loss_rate,
        0.0,
        1.0,
    )

    heartbeat_failure = clamp(
        heartbeat_failure,
        0.0,
        1.0,
    )

    latency_ms = max(
        0.0,
        float(latency_ms),
    )

    if (
        heartbeat_failure >= 1.0
        or packet_loss_rate >= 0.80
    ):
        return "DISCONNECTED"

    if (
        heartbeat_failure > 0.0
        or packet_loss_rate >= 0.20
        or latency_ms >= 250.0
    ):
        return "DEGRADED"

    return "CONNECTED"


def compute_resilience_score(
    *,
    predictive_risk: float,
    uncertainty: float,
    integrity_score: float,
    sensor_plausibility_score: float,
    connectivity_penalty: float,
) -> float:
    """
    Produce a normalized resilience indicator.

    Higher score means better observed resilience.

    This is an EdgeResilience deterministic policy metric,
    not a learned probability.
    """

    predictive_risk = clamp(
        predictive_risk
    )

    uncertainty = clamp(
        uncertainty
    )

    integrity_score = clamp(
        integrity_score
    )

    sensor_plausibility_score = clamp(
        sensor_plausibility_score
    )

    connectivity_penalty = clamp(
        connectivity_penalty
    )

    risk_component = 1.0 - predictive_risk
    uncertainty_component = 1.0 - uncertainty
    connectivity_component = 1.0 - connectivity_penalty

    score = (
        0.35 * risk_component
        + 0.15 * uncertainty_component
        + 0.25 * integrity_score
        + 0.15 * sensor_plausibility_score
        + 0.10 * connectivity_component
    )

    return clamp(score)


def derive_risk_state(
    prediction: Mapping[str, Any],
    *,
    uncertainty_score: float = 0.0,
    packet_loss_rate: float = 0.0,
    latency_ms: float = 0.0,
    heartbeat_failure: float = 0.0,
    integrity_score: float = 1.0,
    sensor_plausibility_score: float = 1.0,
) -> RiskState:
    """
    Convert predictive and system observations into a
    deterministic resilience state.
    """

    y3_probability = clamp(
        float(
            prediction.get(
                "y3_probability",
                0.0,
            )
        )
    )

    y6_probability = clamp(
        float(
            prediction.get(
                "y6_probability",
                0.0,
            )
        )
    )

    predictive_risk = max(
        y3_probability,
        y6_probability,
    )

    predictive_risk_level = probability_to_level(
        predictive_risk
    )

    uncertainty_score = clamp(
        uncertainty_score
    )

    confidence_level = uncertainty_to_confidence(
        uncertainty_score
    )

    connection = connectivity_state(
        packet_loss_rate=packet_loss_rate,
        latency_ms=latency_ms,
        heartbeat_failure=heartbeat_failure,
    )

    integrity_score = clamp(
        integrity_score
    )

    sensor_plausibility_score = clamp(
        sensor_plausibility_score
    )

    if connection == "CONNECTED":
        connectivity_penalty = 0.0
    elif connection == "DEGRADED":
        connectivity_penalty = 0.5
    else:
        connectivity_penalty = 1.0

    resilience = compute_resilience_score(
        predictive_risk=predictive_risk,
        uncertainty=uncertainty_score,
        integrity_score=integrity_score,
        sensor_plausibility_score=sensor_plausibility_score,
        connectivity_penalty=connectivity_penalty,
    )

    reasons: list[str] = []

    if y3_probability >= 0.50:
        reasons.append("Y3_PREDICTIVE_RISK")

    if y6_probability >= 0.50:
        reasons.append("Y6_PREDICTIVE_RISK")

    if uncertainty_score >= 0.75:
        reasons.append("HIGH_UNCERTAINTY")

    if connection == "DEGRADED":
        reasons.append("CONNECTIVITY_DEGRADED")

    if connection == "DISCONNECTED":
        reasons.append("CONNECTIVITY_LOSS")

    if integrity_score < 0.80:
        reasons.append("INTEGRITY_DEGRADATION")

    if sensor_plausibility_score < 0.80:
        reasons.append("SENSOR_PLAUSIBILITY_DEGRADATION")

    evidence_required = bool(
        reasons
        or predictive_risk_level in {
            "HIGH",
            "CRITICAL",
        }
    )

    return RiskState(
        y3_probability=y3_probability,
        y6_probability=y6_probability,
        predictive_risk_level=predictive_risk_level,
        uncertainty_score=uncertainty_score,
        confidence_level=confidence_level,
        connectivity_state=connection,
        integrity_score=integrity_score,
        sensor_plausibility_score=sensor_plausibility_score,
        resilience_score=resilience,
        evidence_required=evidence_required,
        reason_codes=tuple(reasons),
    )
