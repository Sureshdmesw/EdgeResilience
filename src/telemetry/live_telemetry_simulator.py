import json
import math
import random
import time
from pathlib import Path


FEATURE_NAMES = [
    "cyber_message_rate",
    "cyber_unique_can_id_count",
    "cyber_can_id_entropy",
    "cyber_mean_interarrival_ms",
    "cyber_std_interarrival_ms",
    "cyber_min_interarrival_ms",
    "cyber_max_interarrival_ms",
    "cyber_interarrival_cv",
    "cyber_payload_change_rate",
    "cyber_mean_hamming_distance",
    "cyber_dlc_change_rate",
    "cyber_dominant_can_id_fraction",
    "cyber_burst_score",
    "cyber_timing_anomaly_score",
    "cyber_payload_anomaly_score",
    "cyber_id_anomaly_score",
    "cyber_attack_score",
]


def generate_frame(t: int, regime: str = "normal") -> dict:
    phase = t / 12.0

    if regime == "normal":
        attack = 0.01 + 0.01 * abs(math.sin(phase))
        timing = 0.02 + 0.01 * abs(math.cos(phase))
        payload = 0.015
        rate = 48.0 + 3.0 * math.sin(phase)

    elif regime == "degrading":
        attack = min(0.9, 0.08 + t * 0.006)
        timing = min(0.85, 0.08 + t * 0.005)
        payload = min(0.75, 0.05 + t * 0.004)
        rate = 48.0 + 12.0 * math.sin(phase)

    else:
        attack = 0.35 + 0.15 * abs(math.sin(phase))
        timing = 0.30 + 0.15 * abs(math.cos(phase))
        payload = 0.25 + 0.10 * abs(math.sin(phase))
        rate = 60.0 + 10.0 * math.sin(phase)

    return {
        "timestamp": time.time(),
        "sequence": t,
        "source": "software_telemetry_simulator",
        "test_type": "software_simulation",
        "physical_vehicle": False,
        "external_can_transmission": False,
        "direct_actuation": False,
        "production_vehicle_connection": False,
        "features": {
            name: value for name, value in zip(
                FEATURE_NAMES,
                [
                    rate,
                    12.0,
                    2.8,
                    20.0,
                    4.0,
                    12.0,
                    38.0,
                    0.20,
                    0.08,
                    1.7,
                    0.02,
                    0.42,
                    0.08,
                    timing,
                    payload,
                    0.04,
                    attack,
                ],
            )
        },
    }


def stream(regime="normal", interval=0.25):
    sequence = 0

    while True:
        event = generate_frame(sequence, regime)
        print(json.dumps(event), flush=True)
        sequence += 1
        time.sleep(interval)


if __name__ == "__main__":
    stream()
