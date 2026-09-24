from __future__ import annotations

from dataclasses import dataclass
from math import log2, sqrt
from typing import Any


CYBER_FEATURES = (
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
)


@dataclass(frozen=True)
class CANFrame:
    timestamp: float
    can_id: str
    dlc: int
    payload: tuple[int, ...]
    label: str


def hamming_distance(
    previous: tuple[int, ...],
    current: tuple[int, ...],
) -> int:
    """Count differing bits across aligned payload bytes."""
    width = max(len(previous), len(current))
    distance = 0

    for index in range(width):
        old = previous[index] if index < len(previous) else 0
        new = current[index] if index < len(current) else 0
        distance += (old ^ new).bit_count()

    return distance


def entropy(values: list[str]) -> float:
    """Shannon entropy in bits."""
    if not values:
        return 0.0

    counts: dict[str, int] = {}

    for value in values:
        counts[value] = counts.get(value, 0) + 1

    total = len(values)

    return -sum(
        (count / total) * log2(count / total)
        for count in counts.values()
        if count
    )


def coefficient_of_variation(values: list[float]) -> float:
    if not values:
        return 0.0

    mean = sum(values) / len(values)

    if mean <= 0.0:
        return 0.0

    variance = sum((value - mean) ** 2 for value in values) / len(values)

    return sqrt(variance) / mean


def parse_hcrl_line(line: str) -> CANFrame:
    """
    Parse one HCRL CSV record.

    Expected structure:
        timestamp,CAN_ID,DLC,<payload bytes...>,flag

    HCRL uses variable row width because DLC determines the number
    of payload bytes.
    """
    fields = [field.strip() for field in line.split(",")]

    if len(fields) < 4:
        raise ValueError("HCRL record has too few fields")

    timestamp = float(fields[0])
    can_id = fields[1].lower().replace("0x", "")
    dlc = int(fields[2])

    expected_width = 3 + dlc + 1

    if len(fields) != expected_width:
        raise ValueError(
            f"Expected {expected_width} fields for DLC={dlc}, "
            f"received {len(fields)}"
        )

    payload = tuple(
        int(value, 16)
        for value in fields[3 : 3 + dlc]
    )

    label = fields[-1]

    return CANFrame(
        timestamp=timestamp,
        can_id=can_id,
        dlc=dlc,
        payload=payload,
        label=label,
    )


def extract_cyber_features(frames: list[CANFrame]) -> dict[str, float]:
    """
    Extract the initial EdgeResilience cyber feature vector.

    This implementation intentionally operates on a supplied observation
    window rather than the complete dataset. It is therefore suitable
    for unit testing before large-scale processing.
    """
    if not frames:
        return {name: 0.0 for name in CYBER_FEATURES}

    timestamps = [frame.timestamp for frame in frames]
    can_ids = [frame.can_id for frame in frames]

    duration = max(timestamps[-1] - timestamps[0], 1e-9)

    message_rate = len(frames) / duration

    unique_ids = len(set(can_ids))

    id_entropy = entropy(can_ids)

    interarrival_ms = [
        max(frames[index].timestamp - frames[index - 1].timestamp, 0.0)
        * 1000.0
        for index in range(1, len(frames))
    ]

    if interarrival_ms:
        mean_interarrival = sum(interarrival_ms) / len(interarrival_ms)
        variance = sum(
            (value - mean_interarrival) ** 2
            for value in interarrival_ms
        ) / len(interarrival_ms)

        std_interarrival = sqrt(variance)
        min_interarrival = min(interarrival_ms)
        max_interarrival = max(interarrival_ms)
        interarrival_cv = coefficient_of_variation(interarrival_ms)
    else:
        mean_interarrival = 0.0
        std_interarrival = 0.0
        min_interarrival = 0.0
        max_interarrival = 0.0
        interarrival_cv = 0.0

    payload_changes = 0
    hamming_values: list[float] = []
    dlc_changes = 0

    previous_by_id: dict[str, CANFrame] = {}

    for frame in frames:
        previous = previous_by_id.get(frame.can_id)

        if previous is not None:
            if previous.payload != frame.payload:
                payload_changes += 1

            hamming_values.append(
                float(
                    hamming_distance(
                        previous.payload,
                        frame.payload,
                    )
                )
            )

            if previous.dlc != frame.dlc:
                dlc_changes += 1

        previous_by_id[frame.can_id] = frame

    comparisons = max(len(frames) - len(set(can_ids)), 1)

    payload_change_rate = payload_changes / comparisons

    mean_hamming = (
        sum(hamming_values) / len(hamming_values)
        if hamming_values
        else 0.0
    )

    dlc_change_rate = dlc_changes / comparisons

    counts: dict[str, int] = {}

    for can_id in can_ids:
        counts[can_id] = counts.get(can_id, 0) + 1

    dominant_count = max(counts.values())

    dominant_fraction = dominant_count / len(frames)

    # A simple normalized burst indicator:
    # high message density relative to the window duration increases
    # the score. This is deliberately a transparent heuristic.
    burst_score = min(message_rate / 1000.0, 1.0)

    # Initial timing anomaly heuristic.
    timing_anomaly_score = min(interarrival_cv / 5.0, 1.0)

    # Initial payload anomaly heuristic.
    payload_anomaly_score = min(mean_hamming / 32.0, 1.0)

    # Initial CAN-ID concentration/anomaly heuristic.
    id_anomaly_score = min(
        dominant_fraction * 2.0,
        1.0,
    )

    # IMPORTANT:
    # This first implementation deliberately does not use the HCRL
    # attack label to calculate cyber_attack_score.
    #
    # The score is a telemetry-derived composite and will be replaced
    # or calibrated after validation.
    attack_score = min(
        0.30 * burst_score
        + 0.25 * timing_anomaly_score
        + 0.25 * payload_anomaly_score
        + 0.20 * id_anomaly_score,
        1.0,
    )

    return {
        "cyber_message_rate": message_rate,
        "cyber_unique_can_id_count": float(unique_ids),
        "cyber_can_id_entropy": id_entropy,
        "cyber_mean_interarrival_ms": mean_interarrival,
        "cyber_std_interarrival_ms": std_interarrival,
        "cyber_min_interarrival_ms": min_interarrival,
        "cyber_max_interarrival_ms": max_interarrival,
        "cyber_interarrival_cv": interarrival_cv,
        "cyber_payload_change_rate": payload_change_rate,
        "cyber_mean_hamming_distance": mean_hamming,
        "cyber_dlc_change_rate": dlc_change_rate,
        "cyber_dominant_can_id_fraction": dominant_fraction,
        "cyber_burst_score": burst_score,
        "cyber_timing_anomaly_score": timing_anomaly_score,
        "cyber_payload_anomaly_score": payload_anomaly_score,
        "cyber_id_anomaly_score": id_anomaly_score,
        "cyber_attack_score": attack_score,
    }
