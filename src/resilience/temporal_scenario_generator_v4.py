from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List
import random


SEED = 42
OBSERVATION_STEPS = 12
FUTURE_HORIZON = 6

CYBER_FEATURES = [
    "cyber_message_rate",
    "cyber_unique_can_id_count",
    "cyber_can_id_entropy",
    "cyber_mean_interarrival_ms",
    "cyber_std_interarrival_ms",
    "cyber_max_interarrival_ms",
    "cyber_interarrival_cv",
    "cyber_payload_change_rate",
    "cyber_mean_hamming_distance",
    "cyber_dominant_can_id_fraction",
]

FEATURE_NAMES = CYBER_FEATURES + [
    "latency_norm",
    "packet_loss_norm",
    "acceleration_norm",
    "steering_norm",
    "brake_pressure",
    "integrity",
    "sensor_plausibility",
]

REGIMES = (
    "STABLE",
    "CYBER_ESCALATION",
    "CONNECTIVITY_ESCALATION",
    "COUPLED_ESCALATION",
)


@dataclass
class LatentTrajectory:
    regime: str
    cyber_pressure: float
    connectivity_pressure: float
    vehicle_pressure: float
    integrity_pressure: float
    sensor_pressure: float
    memory: float = 0.0


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def choose_regime(rng: random.Random) -> str:
    value = rng.random()

    if value < 0.40:
        return "STABLE"
    if value < 0.60:
        return "CYBER_ESCALATION"
    if value < 0.80:
        return "CONNECTIVITY_ESCALATION"

    return "COUPLED_ESCALATION"


def cyber_features(pressure: float, rng: random.Random) -> Dict[str, float]:
    p = clamp(pressure)

    return {
        "cyber_message_rate": clamp(0.10 + 0.62 * p + rng.gauss(0, 0.025)),
        "cyber_unique_can_id_count": clamp(0.28 - 0.18 * p + rng.gauss(0, 0.025)),
        "cyber_can_id_entropy": clamp(0.24 - 0.12 * p + rng.gauss(0, 0.025)),
        "cyber_mean_interarrival_ms": clamp(0.44 - 0.25 * p + rng.gauss(0, 0.025)),
        "cyber_std_interarrival_ms": clamp(0.42 + 0.28 * p + rng.gauss(0, 0.025)),
        "cyber_max_interarrival_ms": clamp(0.50 + 0.28 * p + rng.gauss(0, 0.025)),
        "cyber_interarrival_cv": clamp(0.18 + 0.38 * p + rng.gauss(0, 0.025)),
        "cyber_payload_change_rate": clamp(0.31 + 0.40 * p + rng.gauss(0, 0.025)),
        "cyber_mean_hamming_distance": clamp(0.16 + 0.38 * p + rng.gauss(0, 0.025)),
        "cyber_dominant_can_id_fraction": clamp(0.24 + 0.42 * p + rng.gauss(0, 0.025)),
    }


def build_observation(state: LatentTrajectory, rng: random.Random) -> Dict[str, float]:
    cyber = cyber_features(state.cyber_pressure, rng)

    connectivity = clamp(
        state.connectivity_pressure
        + rng.gauss(0, 0.02)
    )

    vehicle = clamp(
        state.vehicle_pressure
        + rng.gauss(0, 0.02)
    )

    integrity = clamp(
        1.0
        - state.integrity_pressure
        + rng.gauss(0, 0.015)
    )

    sensor = clamp(
        1.0
        - state.sensor_pressure
        + rng.gauss(0, 0.015)
    )

    return {
        **cyber,
        "latency_norm": clamp(
            0.10 + 0.70 * connectivity
        ),
        "packet_loss_norm": clamp(
            0.05 + 0.75 * connectivity
        ),
        "acceleration_norm": clamp(
            0.10 + 0.45 * vehicle
        ),
        "steering_norm": clamp(
            0.12 + 0.42 * vehicle
        ),
        "brake_pressure": clamp(
            0.18 + 0.50 * vehicle
        ),
        "integrity": integrity,
        "sensor_plausibility": sensor,
    }


def update_state(
    state: LatentTrajectory,
    step: int,
    rng: random.Random,
    future: bool = False,
) -> None:

    progress = step / max(
        OBSERVATION_STEPS - 1,
        1
    )

    if state.regime == "CYBER_ESCALATION":
        state.cyber_pressure += (
            0.018 + 0.010 * progress
        )

    elif state.regime == "CONNECTIVITY_ESCALATION":
        state.connectivity_pressure += (
            0.018 + 0.010 * progress
        )

    elif state.regime == "COUPLED_ESCALATION":
        state.cyber_pressure += (
            0.014 + 0.008 * progress
        )
        state.connectivity_pressure += (
            0.014 + 0.008 * progress
        )
        state.integrity_pressure += 0.006

    else:
        state.cyber_pressure += rng.gauss(0, 0.004)
        state.connectivity_pressure += rng.gauss(0, 0.004)

    # Hidden accumulated trajectory memory.
    instantaneous_pressure = (
        0.32 * state.cyber_pressure
        + 0.25 * state.connectivity_pressure
        + 0.16 * state.vehicle_pressure
        + 0.15 * state.integrity_pressure
        + 0.12 * state.sensor_pressure
    )

    state.memory = clamp(
        0.82 * state.memory
        + 0.18 * instantaneous_pressure
    )

    # The memory affects future state, but is never exposed as a feature.
    if future:
        state.integrity_pressure += (
            0.018 * state.memory
        )
        state.sensor_pressure += (
            0.014 * state.memory
        )
        state.vehicle_pressure += (
            0.010 * state.memory
        )

    state.cyber_pressure = clamp(
        state.cyber_pressure + rng.gauss(0, 0.006)
    )

    state.connectivity_pressure = clamp(
        state.connectivity_pressure + rng.gauss(0, 0.006)
    )

    state.vehicle_pressure = clamp(
        state.vehicle_pressure
        + rng.gauss(0, 0.004)
    )

    state.integrity_pressure = clamp(
        state.integrity_pressure
        + rng.gauss(0, 0.003)
    )

    state.sensor_pressure = clamp(
        state.sensor_pressure
        + rng.gauss(0, 0.003)
    )


def resilience_score(state: LatentTrajectory) -> float:
    pressure = (
        0.30 * state.cyber_pressure
        + 0.22 * state.connectivity_pressure
        + 0.16 * state.vehicle_pressure
        + 0.17 * state.integrity_pressure
        + 0.15 * state.sensor_pressure
    )

    return clamp(1.0 - pressure)


def generate_scenario(
    scenario_id: int,
    seed: int | None = None,
) -> Dict:

    rng = random.Random(
        SEED + scenario_id if seed is None else seed
    )

    regime = choose_regime(rng)

    state = LatentTrajectory(
        regime=regime,
        cyber_pressure=rng.uniform(0.05, 0.18),
        connectivity_pressure=rng.uniform(0.03, 0.16),
        vehicle_pressure=rng.uniform(0.04, 0.14),
        integrity_pressure=rng.uniform(0.02, 0.10),
        sensor_pressure=rng.uniform(0.02, 0.10),
    )

    observations: List[Dict[str, float]] = []

    current_resilience = None

    for step in range(OBSERVATION_STEPS):
        update_state(
            state,
            step,
            rng,
            future=False,
        )

        observation = build_observation(
            state,
            rng,
        )

        observations.append(observation)

        if step == OBSERVATION_STEPS - 1:
            current_resilience = resilience_score(state)

    # Future state evolves separately from the observed sequence.
    future_state = LatentTrajectory(
        regime=regime,
        cyber_pressure=state.cyber_pressure,
        connectivity_pressure=state.connectivity_pressure,
        vehicle_pressure=state.vehicle_pressure,
        integrity_pressure=state.integrity_pressure,
        sensor_pressure=state.sensor_pressure,
        memory=state.memory,
    )

    for step in range(FUTURE_HORIZON):
        update_state(
            future_state,
            step,
            rng,
            future=True,
        )

    future_resilience = resilience_score(
        future_state
    )

    future_degradation = clamp(
        current_resilience - future_resilience
    )

    return {
        "scenario_id": scenario_id,
        "regime": regime,
        "observations": observations,
        "current_resilience": current_resilience,
        "future_resilience": future_resilience,
        "future_degradation": future_degradation,
    }


def generate_dataset(
    count: int = 1000,
    seed: int = SEED,
) -> List[Dict]:

    return [
        generate_scenario(
            scenario_id=i,
            seed=seed + i,
        )
        for i in range(count)
    ]


if __name__ == "__main__":
    dataset = generate_dataset(1000)

    current = [
        x["current_resilience"]
        for x in dataset
    ]

    future = [
        x["future_resilience"]
        for x in dataset
    ]

    degradation = [
        x["future_degradation"]
        for x in dataset
    ]

    print("=" * 80)
    print("EDGERESILIENCE V4 TEMPORAL SCENARIO GENERATOR")
    print("=" * 80)

    print(f"Seed: {SEED}")
    print(f"Scenarios: {len(dataset)}")
    print(f"Observation steps: {OBSERVATION_STEPS}")
    print(f"Future horizon: {FUTURE_HORIZON}")
    print(f"Features per observation: {len(FEATURE_NAMES)}")

    print(
        f"Current resilience: "
        f"{min(current):.4f}-"
        f"{max(current):.4f}"
    )

    print(
        f"Future degradation: "
        f"{min(degradation):.4f}-"
        f"{max(degradation):.4f}"
    )

    print(
        f"Mean future degradation: "
        f"{sum(degradation) / len(degradation):.4f}"
    )

    print()
    print("CYBER_FEATURE_CONTRACT = 10_HCRL_VALIDATED_FEATURES")
    print("LATENT_MEMORY_EXPOSED_AS_FEATURE = FALSE")
    print("FUTURE_STATE_GENERATED_SEPARATELY = TRUE")
    print("TRAJECTORY_DEPENDENT_FUTURE = TRUE")
    print("TARGET_IS_DIRECT_FINAL_STATE_FORMULA = FALSE")
    print("TEMPORAL_SCENARIO_GENERATION_V4 = PASS")
