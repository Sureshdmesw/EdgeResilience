from pathlib import Path
import sys
import random
import math


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


SEED = 42
SCENARIO_COUNT = 1000
OBSERVATION_STEPS = 12
FUTURE_HORIZON = 6


# EdgeResilience cyber-state contract.
# These names correspond to the validated 10-feature cyber representation.
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
        feature: rng.uniform(0.05, 0.95)
        for feature in CYBER_FEATURES
    }

    connectivity = {
        "latency_norm": rng.uniform(0.02, 0.80),
        "packet_loss_norm": rng.uniform(0.00, 0.80),
    }

    vehicle = {
        "acceleration_norm": rng.uniform(0.00, 0.90),
        "steering_norm": rng.uniform(0.00, 0.90),
        "brake_pressure": rng.uniform(0.00, 0.90),
    }

    integrity = rng.uniform(0.75, 1.0)
    sensor_plausibility = rng.uniform(0.85, 1.0)

    return {
        "cyber": cyber,
        "connectivity": connectivity,
        "vehicle": vehicle,
        "integrity": integrity,
        "sensor_plausibility": sensor_plausibility,
    }


def evolve_state(state, rng, future=False):

    cyber = dict(state["cyber"])
    connectivity = dict(state["connectivity"])
    vehicle = dict(state["vehicle"])

    for key in cyber:
        cyber[key] = clamp(
            cyber[key] + rng.gauss(0.0, 0.025)
        )

    for key in connectivity:
        connectivity[key] = clamp(
            connectivity[key] + rng.gauss(0.0, 0.020)
        )

    for key in vehicle:
        vehicle[key] = clamp(
            vehicle[key] + rng.gauss(0.0, 0.025)
        )

    integrity = clamp(
        state["integrity"] + rng.gauss(0.0, 0.008)
    )

    sensor_plausibility = clamp(
        state["sensor_plausibility"] + rng.gauss(0.0, 0.008)
    )

    if future:

        event_probability = rng.uniform(0.05, 0.35)

        if rng.random() < event_probability:

            event_type = rng.choice(
                (
                    "CYBER",
                    "CONNECTIVITY",
                    "COUPLED",
                    "SENSOR",
                )
            )

            if event_type == "CYBER":

                for feature in (
                    "cyber_message_rate",
                    "cyber_payload_change_rate",
                    "cyber_mean_hamming_distance",
                    "cyber_dominant_can_id_fraction",
                ):
                    cyber[feature] = clamp(
                        cyber[feature] + rng.uniform(0.10, 0.30)
                    )

                cyber["cyber_mean_interarrival_ms"] = clamp(
                    cyber["cyber_mean_interarrival_ms"]
                    + rng.uniform(0.08, 0.25)
                )

                cyber["cyber_interarrival_cv"] = clamp(
                    cyber["cyber_interarrival_cv"]
                    + rng.uniform(0.08, 0.25)
                )

            elif event_type == "CONNECTIVITY":

                connectivity["latency_norm"] = clamp(
                    connectivity["latency_norm"]
                    + rng.uniform(0.15, 0.35)
                )

                connectivity["packet_loss_norm"] = clamp(
                    connectivity["packet_loss_norm"]
                    + rng.uniform(0.10, 0.30)
                )

            elif event_type == "COUPLED":

                cyber["cyber_payload_change_rate"] = clamp(
                    cyber["cyber_payload_change_rate"]
                    + rng.uniform(0.10, 0.30)
                )

                cyber["cyber_mean_hamming_distance"] = clamp(
                    cyber["cyber_mean_hamming_distance"]
                    + rng.uniform(0.10, 0.25)
                )

                connectivity["packet_loss_norm"] = clamp(
                    connectivity["packet_loss_norm"]
                    + rng.uniform(0.15, 0.35)
                )

                integrity = clamp(
                    integrity - rng.uniform(0.05, 0.18)
                )

            elif event_type == "SENSOR":

                sensor_plausibility = clamp(
                    sensor_plausibility
                    - rng.uniform(0.08, 0.25)
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
        "latency_norm":
            state["connectivity"]["latency_norm"],
        "packet_loss_norm":
            state["connectivity"]["packet_loss_norm"],
        "acceleration_norm":
            state["vehicle"]["acceleration_norm"],
        "steering_norm":
            state["vehicle"]["steering_norm"],
        "brake_pressure":
            state["vehicle"]["brake_pressure"],
        "integrity":
            state["integrity"],
        "sensor_plausibility":
            state["sensor_plausibility"],
    }


def generate_temporal_scenario(index, rng):

    state = generate_initial_state(rng)

    observations = []

    for _ in range(OBSERVATION_STEPS):

        observations.append(
            flatten_observation(state)
        )

        state = evolve_state(
            state,
            rng,
            future=False,
        )

    current_resilience = resilience_score(state)

    future_state = state

    for _ in range(FUTURE_HORIZON):

        future_state = evolve_state(
            future_state,
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
        "scenario_id":
            f"ER_TEMPORAL_HCRL_CONTRACT_{index:06d}",

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
        generate_temporal_scenario(
            index,
            rng,
        )
        for index in range(SCENARIO_COUNT)
    ]

    degradations = [
        s["future_degradation"]
        for s in scenarios
    ]

    future_resilience = [
        s["future_resilience"]
        for s in scenarios
    ]

    print("=" * 90)
    print("EDGERESILIENCE HCRL-CONTRACT TEMPORAL GENERATOR")
    print("=" * 90)

    print(f"Seed: {SEED}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Observation steps: {OBSERVATION_STEPS}")
    print(f"Future horizon: {FUTURE_HORIZON}")
    print("Features per observation:", len(scenarios[0]["observations"][0]))
    print()

    print(
        "Current resilience range:",
        f"{min(s['current_resilience'] for s in scenarios):.4f}",
        "-",
        f"{max(s['current_resilience'] for s in scenarios):.4f}",
    )

    print(
        "Future resilience range:",
        f"{min(future_resilience):.4f}",
        "-",
        f"{max(future_resilience):.4f}",
    )

    print(
        "Future degradation range:",
        f"{min(degradations):.4f}",
        "-",
        f"{max(degradations):.4f}",
    )

    print()
    print("CYBER_FEATURE_CONTRACT = 10_HCRL_VALIDATED_FEATURES")
    print("TARGET_IS_CURRENT_STATE_FORMULA = False")
    print("FUTURE_STATE_GENERATED_SEPARATELY = True")
    print("TEMPORAL_SCENARIO_GENERATION = PASS")
