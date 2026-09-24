from pathlib import Path
from collections import Counter
import sys
import statistics

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ai.hcrl_cyber_features import (
    extract_cyber_features,
    parse_hcrl_line,
)

ROOT = Path(
    r"E:\Predictive Cyber-Physical Resilience for Safety-Critical "
    r"Connected Vehicles\data\raw\real_cyber_telemetry"
    r"\hcrl_car_hacking"
)

DATASETS = (
    ("DoS_dataset.csv", "DOS"),
    ("Fuzzy_dataset.csv", "FUZZY"),
    ("gear_dataset.csv", "GEAR_SPOOFING"),
    ("RPM_dataset.csv", "RPM_SPOOFING"),
)

WINDOW_SIZES = (50, 100, 200, 500)
WINDOWS_PER_DATASET = 100


def read_frames(path, limit=None):
    frames = []

    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.strip():
                continue

            try:
                frame = parse_hcrl_line(line)
            except Exception:
                continue

            frames.append(frame)

            if limit is not None and len(frames) >= limit:
                break

    return frames


def summarize_windows(frames, window_size):
    rows = []

    for start in range(
        0,
        len(frames) - window_size + 1,
        window_size,
    ):
        window = frames[start:start + window_size]

        labels = [frame.label for frame in window]
        counts = Counter(labels)

        t_fraction = counts.get("T", 0) / len(window)
        r_fraction = counts.get("R", 0) / len(window)

        features = extract_cyber_features(window)

        rows.append(
            {
                "t_fraction": t_fraction,
                "r_fraction": r_fraction,
                "message_rate": features["cyber_message_rate"],
                "unique_ids": features["cyber_unique_can_id_count"],
                "entropy": features["cyber_can_id_entropy"],
                "interarrival_cv": features["cyber_interarrival_cv"],
                "payload_change": features["cyber_payload_change_rate"],
                "hamming": features["cyber_mean_hamming_distance"],
                "dominant_fraction": features[
                    "cyber_dominant_can_id_fraction"
                ],
            }
        )

        if len(rows) >= WINDOWS_PER_DATASET:
            break

    return rows


def mean(values):
    return statistics.mean(values) if values else 0.0


def std(values):
    return statistics.stdev(values) if len(values) > 1 else 0.0


print("=" * 100)
print("EDGERESILIENCE HCRL WINDOW-SCALE ANALYSIS")
print("=" * 100)

for filename, dataset_name in DATASETS:

    path = ROOT / filename

    # Enough records for all requested scales.
    frames = read_frames(path, limit=250000)

    print()
    print(f"[{dataset_name}]")
    print(f"Loaded frames: {len(frames):,}")

    for window_size in WINDOW_SIZES:

        rows = summarize_windows(frames, window_size)

        t_fractions = [r["t_fraction"] for r in rows]
        message_rates = [r["message_rate"] for r in rows]
        entropies = [r["entropy"] for r in rows]
        payload_changes = [r["payload_change"] for r in rows]
        hamming = [r["hamming"] for r in rows]
        dominant = [r["dominant_fraction"] for r in rows]

        mixed = sum(
            0.0 < value < 1.0
            for value in t_fractions
        )

        attack_heavy = sum(
            value >= 0.50
            for value in t_fractions
        )

        normal_heavy = sum(
            value < 0.50
            for value in t_fractions
        )

        print()
        print(f"  Window = {window_size} frames")
        print(f"    Windows analyzed: {len(rows)}")
        print(f"    Mixed-label windows: {mixed}")
        print(f"    T-dominant windows: {attack_heavy}")
        print(f"    R-dominant windows: {normal_heavy}")

        print(
            f"    T fraction: "
            f"mean={mean(t_fractions):.4f}, "
            f"std={std(t_fractions):.4f}, "
            f"min={min(t_fractions):.4f}, "
            f"max={max(t_fractions):.4f}"
        )

        print(
            f"    Message rate: "
            f"mean={mean(message_rates):.3f}, "
            f"std={std(message_rates):.3f}"
        )

        print(
            f"    CAN-ID entropy: "
            f"mean={mean(entropies):.3f}, "
            f"std={std(entropies):.3f}"
        )

        print(
            f"    Payload change: "
            f"mean={mean(payload_changes):.4f}, "
            f"std={std(payload_changes):.4f}"
        )

        print(
            f"    Mean Hamming: "
            f"mean={mean(hamming):.3f}, "
            f"std={std(hamming):.3f}"
        )

        print(
            f"    Dominant CAN-ID fraction: "
            f"mean={mean(dominant):.4f}, "
            f"std={std(dominant):.4f}"
        )

print()
print("=" * 100)
print("WINDOW-SCALE ANALYSIS = PASS")
print("=" * 100)
