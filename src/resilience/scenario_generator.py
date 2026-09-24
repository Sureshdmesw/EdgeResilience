from pathlib import Path
from dataclasses import asdict
import sys
import random
import math


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.resilience.scenario_schema import (
    VehicleState,
    ConnectivityState,
    CyberPhysicalScenario,
    validate_scenario,
)


SEED = 42
SCENARIO_COUNT = 1000


def clamp(value, low=0.0, high=1.0):
    return max(low, min(high, value))


def sigmoid(value):
    return 1.0 / (1.0 + math.exp(-value))


def generate_vehicle_state(rng):
    speed = rng.uniform(0.0, 120.0)

    acceleration = rng.uniform(
        -4.0,
        3.5,
    )

    steering = rng.uniform(
        -25.0,
        25.0,
    )

    brake_pressure = rng.uniform(
        0.0,
        1.0,
    )

    sensor_plausibility = rng.uniform(
        0.92,
        1.0,
    )

    return VehicleState(
        speed_kph=speed,
        acceleration_mps2=acceleration,
        steering_angle_deg=steering,
        brake_pressure=brake_pressure,
        sensor_plausibility_score=sensor_plausibility,
    )


def generate_connectivity_state(rng):
    latency = rng.uniform(
        10.0,
        180.0,
    )

    packet_loss = rng.uniform(
        0.0,
        0.12,
    )

    heartbeat_failure = False

    rssi = rng.uniform(
        -75.0,
        -45.0,
    )

    return ConnectivityState(
        latency_ms=latency,
        packet_loss_rate=packet_loss,
        heartbeat_failure=heartbeat_failure,
        rssi_dbm=rssi,
    )


def generate_cyber_state(rng):
    return {
        "cyber_message_rate": rng.uniform(
            800.0,
            2400.0,
        ),
        "cyber_unique_can_id_count": rng.uniform(
            10.0,
            65.0,
        ),
        "cyber_can_id_entropy": rng.uniform(
            2.5,
            5.5,
        ),
        "cyber_mean_interarrival_ms": rng.uniform(
            0.4,
            2.0,
        ),
        "cyber_std_interarrival_ms": rng.uniform(
            0.2,
            2.0,
        ),
        "cyber_max_interarrival_ms": rng.uniform(
            1.0,
            8.0,
        ),
        "cyber_interarrival_cv": rng.uniform(
            0.4,
            2.0,
        ),
        "cyber_payload_change_rate": rng.uniform(
            0.15,
            0.65,
        ),
        "cyber_mean_hamming_distance": rng.uniform(
            1.0,
            4.5,
        ),
        "cyber_dominant_can_id_fraction": rng.uniform(
            0.05,
            0.55,
        ),
    }


def generate_scenario(index, rng):

    vehicle = generate_vehicle_state(rng)
    connectivity = generate_connectivity_state(rng)
    cyber = generate_cyber_state(rng)

    cyber_pressure = clamp(
        0.25 * cyber["cyber_message_rate"] / 2400.0
        + 0.20 * cyber["cyber_interarrival_cv"] / 2.0
        + 0.20 * cyber["cyber_payload_change_rate"]
        + 0.20 * cyber["cyber_mean_hamming_distance"] / 4.5
        + 0.15 * (
            1.0
            - cyber["cyber_dominant_can_id_fraction"]
        )
    )

    connectivity_pressure = clamp(
        0.55 * connectivity.packet_loss_rate / 0.12
        + 0.45 * connectivity.latency_ms / 180.0
    )

    vehicle_pressure = clamp(
        0.45 * abs(vehicle.acceleration_mps2) / 4.0
        + 0.30 * abs(vehicle.steering_angle_deg) / 25.0
        + 0.25 * vehicle.brake_pressure
    )

    interaction_pressure = (
        cyber_pressure
        * connectivity_pressure
    )

    degradation = clamp(
        0.35 * cyber_pressure
        + 0.25 * connectivity_pressure
        + 0.15 * vehicle_pressure
        + 0.25 * interaction_pressure
    )

    future_resilience = clamp(
        1.0 - degradation
    )

    integrity_score = clamp(
        1.0
        - 0.35 * cyber_pressure
        - 0.20 * connectivity_pressure
        + rng.uniform(-0.02, 0.02)
    )

    sensor_plausibility = clamp(
        vehicle.sensor_plausibility_score
        - 0.20 * interaction_pressure
    )

    if degradation >= 0.70:
        scenario_state = "RESILIENCE_DEGRADED"
    elif (
        cyber_pressure >= 0.60
        and connectivity_pressure >= 0.60
    ):
        scenario_state = "CYBER_CONNECTIVITY_DEGRADED"
    elif cyber_pressure >= 0.60:
        scenario_state = "CYBER_DEGRADED"
    elif connectivity_pressure >= 0.60:
        scenario_state = "CONNECTIVITY_DEGRADED"
    else:
        scenario_state = "NORMAL"

    scenario = CyberPhysicalScenario(
        scenario_id=f"ER_SCENARIO_{index:06d}",
        cyber_state=cyber,
        vehicle_state=VehicleState(
            speed_kph=vehicle.speed_kph,
            acceleration_mps2=vehicle.acceleration_mps2,
            steering_angle_deg=vehicle.steering_angle_deg,
            brake_pressure=vehicle.brake_pressure,
            sensor_plausibility_score=sensor_plausibility,
        ),
        connectivity_state=connectivity,
        integrity_score=integrity_score,
        future_resilience_score=future_resilience,
        resilience_degradation=degradation,
        scenario_state=scenario_state,
    )

    validate_scenario(scenario)

    return scenario


if __name__ == "__main__":

    rng = random.Random(SEED)

    scenarios = [
        generate_scenario(
            index,
            rng,
        )
        for index in range(SCENARIO_COUNT)
    ]

    states = {}

    for scenario in scenarios:
        states[scenario.scenario_state] = (
            states.get(
                scenario.scenario_state,
                0,
            )
            + 1
        )

    resilience = [
        scenario.future_resilience_score
        for scenario in scenarios
    ]

    degradation = [
        scenario.resilience_degradation
        for scenario in scenarios
    ]

    print("=" * 90)
    print("EDGERESILIENCE SCENARIO GENERATOR")
    print("=" * 90)
    print(f"Seed: {SEED}")
    print(f"Scenarios: {len(scenarios)}")
    print()
    print("Scenario states:")
    for state, count in sorted(states.items()):
        print(f"  {state}: {count}")

    print()
    print(
        "Future resilience range:",
        f"{min(resilience):.4f}",
        "-",
        f"{max(resilience):.4f}",
    )

    print(
        "Degradation range:",
        f"{min(degradation):.4f}",
        "-",
        f"{max(degradation):.4f}",
    )

    print()
    print("SCENARIO_GENERATION = PASS")
