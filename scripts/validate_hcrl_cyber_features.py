from pathlib import Path
from collections import defaultdict
from statistics import mean
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ai.hcrl_cyber_features import (
    CYBER_FEATURES,
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

WINDOW_SIZE = 200
MAX_WINDOWS_PER_DATASET = 20


def read_windows(path: Path):
    window = []
    window_count = 0

    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.strip():
                continue

            try:
                frame = parse_hcrl_line(line)
            except Exception:
                continue

            window.append(frame)

            if len(window) == WINDOW_SIZE:
                yield window
                window = []
                window_count += 1

                if window_count >= MAX_WINDOWS_PER_DATASET:
                    break


summary = {}

for filename, label in DATASETS:
    path = ROOT / filename

    feature_rows = list(
        extract_cyber_features(window)
        for window in read_windows(path)
    )

    if not feature_rows:
        raise RuntimeError(f"No windows extracted from {filename}")

    summary[label] = {}

    for feature in CYBER_FEATURES:
        values = [row[feature] for row in feature_rows]

        summary[label][feature] = {
            "mean": mean(values),
            "min": min(values),
            "max": max(values),
        }


print("HCRL FEATURE QUALITY SAMPLE")
print("=" * 70)
print(f"Window size: {WINDOW_SIZE}")
print(f"Windows per dataset: {MAX_WINDOWS_PER_DATASET}")

for label in summary:
    print(f"\n[{label}]")

    for feature in CYBER_FEATURES:
        stats = summary[label][feature]

        print(
            f"{feature:35s} "
            f"mean={stats['mean']:.6f} "
            f"min={stats['min']:.6f} "
            f"max={stats['max']:.6f}"
        )

print("\nFEATURE_QUALITY_SAMPLE = PASS")
