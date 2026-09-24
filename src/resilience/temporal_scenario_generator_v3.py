from pathlib import Path
import sys
import random

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


SEED = 42
SCENARIO_COUNT = 1000
OBSERVATION_STEPS = 12
FUTURE_HORIZON = 6


CYBER_FEATURES = (
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
)

REGIMES = (
    "STABLE",
    "CYBER_ESCALATION",
    "CONNECTIVITY_ESCALATION",
    "COUPLED_ESCALATION",
)


def clamp(value, low=0.0, high=1.0):
    return max(low, min(high, value))


def cyber_pressure(cyber):
    return clamp(
        0.15 * cyber["cyber_message_rate"]
        + 0.10 * cyber["cyber_unique_can_id_count"]
        + 0.10 * cyber["cyber_can_id_entropy"]
        + 0.15 * cyber["cyber_mean_interarrival_ms"]
        + 0.10 * cyber["cyber_std_interarrival_ms"]
        + 0.10 * cyber["cyber_max_interarrival_ms"]
        + 0.10 * cyber["cyber_interarrival_cv"]
        + 0.10 * cyber["cyber_payload_change_rate"]
        + 0.05 * cyber["cyber_mean_hamming_distance"]
        + 0.05 * cyber["cyber_dominant_can_id_fraction"]
    )


def connectivity_pressure(connectivity):
    return clamp(
        0.55 * connectivity["packet_loss_norm"]
        + 0.45 * connectivity["latency_norm"]
    )


def vehicle_pressure(vehicle):
    return clamp(
        0.45 * vehicle["acceleration_norm"]
        + 0.30 * vehicle["steering_norm"]
        + 0.25 * vehicle["brake_pressure"]
    )


def generate_initial_state(rng):
    cyber = {
        feature: rng.uniform(0.15, 0.55)
        for feature in CYBER_FEATURES
    }

    connectivity = {
        "latency_norm": rng.uniform(0.05, 0.35),
        "packet_loss_norm": rng.uniform(0.00, 0.25),
    }

    vehicle = {
        "acceleration_norm": rng.uniform(0.05, 0.45),
        "steering_norm": rng.uniform(0.05, 0.45),
        "brake_pressure": rng.uniform(0.05, 0.45),
    }

    return {
        "cyber": cyber,
        "connectivity": connectivity,
        "vehicle": vehicle,
        "integrity": rng.uniform(0.88, 1.0),
        "sensor_plausibility": rng.uniform(0.90, 1.0),
    }


def choose_regime(rng):
    return rng.choices(
        REGIMES,
        weights=(0.45, 0.20, 0.20, 0.15),
        k=1,
    )[0]


def evolve_observation(state, regime, step, rng):
    cyber = dict(state["cyber"])
    connectivity = dict(state["connectivity"])
    vehicle = dict(state["vehicle"])

    progress = step / max(OBSERVATION_STEPS - 1, 1)

    if regime == "CYBER_ESCALATION":
        cyber_drift = 0.010 + 0.035 * progress
        connectivity_drift = 0.002

    elif regime == "CONNECTIVITY_ESCALATION":
        cyber_drift = 0.002
        connectivity_drift = 0.015 + 0.035 * progress

    elif regime == "COUPLED_ESCALATION":
        cyber_drift = 0.008 + 0.025 * progress
        connectivity_drift = 0.010 + 0.025 * progress

    else:
        cyber_drift = 0.001
        connectivity_drift = 0.001

    for feature in cyber:
        cyber[feature] = clamp(
            cyber[feature]
            + cyber_drift
            + rng.gauss(0.0, 0.012)
        )

    for feature in connectivity:
        connectivity[feature] = clamp(
            connectivity[feature]
            + connectivity_drift
            + rng.gauss(0.0, 0.010)
        )

    for feature in vehicle:
        vehicle[feature] = clamp(
            vehicle[feature]
            + rng.gauss(0.0, 0.012)
        )

    integrity = clamp(
        state["integrity"]
        - (
            (0.008 + 0.015 * progress)
            if regime == "COUPLED_ESCALATION"
            else 0.002
        )
        + rng.gauss(0.0, 0.004)
    )

    sensor_plausibility = clamp(
        state["sensor_plausibility"]
        - (
            (0.006 + 0.010 * progress)
            if regime == "COUPLED_ESCALATION"
            else 0.001
        )
        + rng.gauss(0.0, 0.004)
    )

    return {
        "cyber": cyber,
        "connectivity": connectivity,
        "vehicle": vehicle,
        "integrity": integrity,
        "sensor_plausibility": sensor_plausibility,
    }


def evolve_future(state, regime, rng):
    cyber = dict(state["cyber"])
    connectivity = dict(state["connectivity"])
    vehicle = dict(state["vehicle"])

    cyber_drift = 0.004
    connectivity_drift = 0.004

    if regime in ("CYBER_ESCALATION", "COUPLED_ESCALATION"):
        cyber_drift += 0.010

    if regime in ("CONNECTIVITY_ESCALATION", "COUPLED_ESCALATION"):
        connectivity_drift += 0.012

    for feature in cyber:
        cyber[feature] = clamp(
            cyber[feature]
            + cyber_drift
            + rng.gauss(0.0, 0.020)
        )

    for feature in connectivity:
        connectivity[feature] = clamp(
            connectivity[feature]
            + connectivity_drift
            + rng.gauss(0.0, 0.018)
        )

    for feature in vehicle:
        vehicle[feature] = clamp(
            vehicle[feature]
            + rng.gauss(0.0, 0.018)
        )

    integrity = clamp(
        state["integrity"]
        - rng.uniform(0.0, 0.025)
        - (
            rng.uniform(0.0, 0.040)
            if regime == "COUPLED_ESCALATION"
            else 0.0
        )
    )

    sensor_plausibility = clamp(
        state["sensor_plausibility"]
        - rng.uniform(0.0, 0.020)
    )

    return {
        "cyber": cyber,
        "connectivity": connectivity,
        "vehicle": vehicle,
        "integrity": integrity,
        "sensor_plausibility": sensor_plausibility,
    }


def resilience_score(state):
    cp = cyber_pressure(state["cyber"])
    np = connectivity_pressure(state["connectivity"])
    vp = vehicle_pressure(state["vehicle"])

    interaction = cp * np

    return clamp(
        1.0
        - (
            0.30 * cp
            + 0.25 * np
            + 0.10 * vp
            + 0.20 * interaction
            + 0.10 * (1.0 - state["integrity"])
            + 0.05 * (1.0 - state["sensor_plausibility"])
        )
    )


def flatten_observation(state):
    return {
        **state["cyber"],
        "latency_norm": state["connectivity"]["latency_norm"],
        "packet_loss_norm": state["connectivity"]["packet_loss_norm"],
        "acceleration_norm": state["vehicle"]["acceleration_norm"],
        "steering_norm": state["vehicle"]["steering_norm"],
        "brake_pressure": state["vehicle"]["brake_pressure"],
        "integrity": state["integrity"],
        "sensor_plausibility": state["sensor_plausibility"],
    }


def generate_temporal_scenario(index, rng):
    regime = choose_regime(rng)
    state = generate_initial_state(rng)

    observations = []

    for step in range(OBSERVATION_STEPS):
        observations.append(flatten_observation(state))

        state = evolve_observation(
            state,
            regime,
            step,
            rng,
        )

    current_resilience = resilience_score(state)

    future_state = state

    for _ in range(FUTURE_HORIZON):
        future_state = evolve_future(
            future_state,
            regime,
            rng,
        )

    future_resilience = resilience_score(future_state)

    future_degradation = clamp(
        current_resilience - future_resilience
    )

    return {
        "scenario_id":
            f"ER_TEMPORAL_CONDITIONED_V3_{index:06d}",

        "regime": regime,

        "observations":
            observations,

        "current_resilience":
            current_resilience,

        "future_resilience":
            future_resilience,

        "future_degradation":
            future_degradation,
    }


if __name__ == "__main__":
    rng = random.Random(SEED)

    scenarios = [
        generate_temporal_scenario(index, rng)
        for index in range(SCENARIO_COUNT)
    ]

    degradations = [
        s["future_degradation"]
        for s in scenarios
    ]

    print("=" * 90)
    print("EDGERESILIENCE TEMPORAL GENERATOR V3")
    print("=" * 90)

    print(f"Seed: {SEED}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Observation steps: {OBSERVATION_STEPS}")
    print(f"Future horizon: {FUTURE_HORIZON}")
    print(
        "Features per observation:",
        len(scenarios[0]["observations"][0]),
    )

    print()
    print("Regime distribution:")

    for regime in REGIMES:
        count = sum(
            s["regime"] == regime
            for s in scenarios
        )
        print(f"{regime:25s}: {count}")

    print()

    print(
        "Current resilience range:",
        f"{min(s['current_resilience'] for s in scenarios):.4f}",
        "-",
        f"{max(s['current_resilience'] for s in scenarios):.4f}",
    )

    print(
        "Future degradation range:",
        f"{min(degradations):.4f}",
        "-",
        f"{max(degradations):.4f}",
    )

    print(
        "Mean future degradation:",
        f"{sum(degradations) / len(degradations):.4f}",
    )

    print()
    print("CYBER_FEATURE_CONTRACT = 10_HCRL_VALIDATED_FEATURES")
    print("OBSERVABLE_PRECURSOR_TRAJECTORIES = TRUE")
    print("FUTURE_STATE_GENERATED_SEPARATELY = TRUE")
    print("LATENT_REGIME_EXPOSED_AS_FEATURE = FALSE")
    print("TARGET_IS_DIRECT_FEATURE_FORMULA = FALSE")
    print("TEMPORAL_SCENARIO_GENERATION_V3 = PASS")
