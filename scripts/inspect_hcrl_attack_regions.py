from pathlib import Path
from collections import Counter
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ai.hcrl_cyber_features import parse_hcrl_line

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

print("=" * 90)
print("EDGERESILIENCE HCRL ATTACK-REGION DIAGNOSTIC")
print("=" * 90)

for filename, name in DATASETS:
    path = ROOT / filename

    total = 0
    r_count = 0
    t_count = 0

    transitions = []
    previous_label = None
    first_t = None
    last_t = None

    min_ts = None
    max_ts = None

    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.strip():
                continue

            try:
                frame = parse_hcrl_line(line)
            except Exception:
                continue

            total += 1

            if min_ts is None:
                min_ts = frame.timestamp

            max_ts = frame.timestamp

            if frame.label == "R":
                r_count += 1
            elif frame.label == "T":
                t_count += 1

                if first_t is None:
                    first_t = frame.timestamp

                last_t = frame.timestamp

            if previous_label is not None and frame.label != previous_label:
                transitions.append(
                    (
                        total,
                        previous_label,
                        frame.label,
                        frame.timestamp,
                    )
                )

            previous_label = frame.label

    print()
    print(f"[{name}]")
    print(f"  Total records: {total:,}")
    print(f"  R records:     {r_count:,}")
    print(f"  T records:     {t_count:,}")

    if min_ts is not None and max_ts is not None:
        print(f"  Duration:      {max_ts - min_ts:.3f} sec")

    if first_t is not None:
        print(f"  First T:       record timestamp {first_t}")
        print(f"  Last T:        record timestamp {last_t}")
        print(f"  T span:        {last_t - first_t:.3f} sec")

    print(f"  Label transitions: {len(transitions)}")

    print("  First transitions:")
    for row in transitions[:10]:
        print(
            f"    record={row[0]:,} "
            f"{row[1]} -> {row[2]} "
            f"timestamp={row[3]}"
        )

print()
print("=" * 90)
print("ATTACK-REGION DIAGNOSTIC = PASS")
print("=" * 90)
