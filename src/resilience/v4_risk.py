from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


V4_RISK_LEVELS = (
    "NORMAL",
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
)


@dataclass(frozen=True)
class V4RiskInterpretation:
    future_degradation: float
    predictive_risk_level: str
    evidence_required: bool
    reason_codes: tuple[str, ...]
    policy_name: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def interpret_v4_degradation(
    future_degradation: float,
) -> V4RiskInterpretation:
    """
    Deterministic interpretation of the EdgeResilience V4
    future-degradation prediction.

    These thresholds are EdgeResilience demo-policy defaults.
    They are not learned thresholds, Snapdragon limits,
    or physical-vehicle safety limits.
    """

    value = max(
        0.0,
        min(1.0, float(future_degradation)),
    )

    if value < 0.02:
        level = "NORMAL"
        evidence_required = False
        reason_codes = ()

    elif value < 0.04:
        level = "LOW"
        evidence_required = False
        reason_codes = (
            "V4_PREDICTED_DEGRADATION_LOW",
        )

    elif value < 0.06:
        level = "MEDIUM"
        evidence_required = True
        reason_codes = (
            "V4_PREDICTED_DEGRADATION_MEDIUM",
        )

    elif value < 0.07:
        level = "HIGH"
        evidence_required = True
        reason_codes = (
            "V4_PREDICTED_DEGRADATION_HIGH",
        )

    else:
        level = "CRITICAL"
        evidence_required = True
        reason_codes = (
            "V4_PREDICTED_DEGRADATION_CRITICAL",
        )

    return V4RiskInterpretation(
        future_degradation=value,
        predictive_risk_level=level,
        evidence_required=evidence_required,
        reason_codes=reason_codes,
        policy_name="V4_DEGRADATION_DEMO_POLICY_V1",
    )
