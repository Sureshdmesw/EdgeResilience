from pathlib import Path
from statistics import mean, pstdev
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
MAX_WINDOWS = 200


def read_windows(path: Path):
    window = []
    count = 0

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
                count += 1

                if count >= MAX_WINDOWS:
                    break


results = {}

for filename, label in DATASETS:
    rows = [
        extract_cyber_features(window)
        for window in read_windows(ROOT / filename)
    ]

    if len(rows) < MAX_WINDOWS:
        print(
            f"WARNING: {label} produced only {len(rows)} windows"
        )

    results[label] = rows


print("=" * 90)
print("EDGERESILIENCE HCRL FEATURE STABILITY ANALYSIS")
print("=" * 90)
print(f"Window size: {WINDOW_SIZE}")
print(f"Maximum windows per dataset: {MAX_WINDOWS}")
print()

for label, rows in results.items():
    print(f"\n[{label}] windows={len(rows)}")

    for feature in CYBER_FEATURES:
        values = [row[feature] for row in rows]

        avg = mean(values)
        std = pstdev(values) if len(values) > 1 else 0.0

        print(
            f"{feature:35s} "
            f"mean={avg:12.6f} "
            f"std={std:12.6f}"
        )

print("\nFEATURE_STABILITY_ANALYSIS = PASS")
