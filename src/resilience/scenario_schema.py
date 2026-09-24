from dataclasses import dataclass, asdict
from typing import Dict


SCENARIO_STATES = (
    "NORMAL",
    "CYBER_DEGRADED",
    "CONNECTIVITY_DEGRADED",
    "CYBER_CONNECTIVITY_DEGRADED",
    "RESILIENCE_DEGRADED",
)


@dataclass(frozen=True)
class VehicleState:
    speed_kph: float
    acceleration_mps2: float
    steering_angle_deg: float
    brake_pressure: float
    sensor_plausibility_score: float


@dataclass(frozen=True)
class ConnectivityState:
    latency_ms: float
    packet_loss_rate: float
    heartbeat_failure: bool
    rssi_dbm: float


@dataclass(frozen=True)
class CyberPhysicalScenario:
    scenario_id: str
    cyber_state: Dict[str, float]
    vehicle_state: VehicleState
    connectivity_state: ConnectivityState
    integrity_score: float
    future_resilience_score: float
    resilience_degradation: float
    scenario_state: str

    def to_dict(self) -> Dict:
        result = asdict(self)
        return result


def validate_scenario(scenario: CyberPhysicalScenario) -> None:
    if scenario.future_resilience_score < 0.0:
        raise ValueError("future_resilience_score < 0")

    if scenario.future_resilience_score > 1.0:
        raise ValueError("future_resilience_score > 1")

    if scenario.resilience_degradation < 0.0:
        raise ValueError("resilience_degradation < 0")

    if scenario.resilience_degradation > 1.0:
        raise ValueError("resilience_degradation > 1")

    if not 0.0 <= scenario.integrity_score <= 1.0:
        raise ValueError("integrity_score outside [0,1]")

    if not 0.0 <= scenario.vehicle_state.sensor_plausibility_score <= 1.0:
        raise ValueError(
            "sensor_plausibility_score outside [0,1]"
        )

    if not 0.0 <= scenario.connectivity_state.packet_loss_rate <= 1.0:
        raise ValueError(
            "packet_loss_rate outside [0,1]"
        )

    if scenario.scenario_state not in SCENARIO_STATES:
        raise ValueError(
            f"Unknown scenario_state: {scenario.scenario_state}"
        )


if __name__ == "__main__":
    print(
        "SCENARIO_STATES =",
        SCENARIO_STATES,
    )

    print(
        "SCENARIO_SCHEMA = PASS"
    )
