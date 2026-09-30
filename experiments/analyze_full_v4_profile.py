import json
from pathlib import Path

p = Path(r"experiments\snapdragon\profile_artifacts\v4_full_production\EdgeResilience V4 QNN-Ready Full Model HTP Profile_jpxlwmxlp_results.json")

with p.open("r", encoding="utf-8") as f:
    data = json.load(f)

print("=" * 80)
print("FULL PRODUCTION V4 PROFILE ANALYSIS")
print("=" * 80)

print("\n=== TOP-LEVEL KEYS ===")
for k in data:
    print(k)

print("\n=== EXECUTION SUMMARY ===")
summary = data.get("execution_summary", {})
for k, v in summary.items():
    print(f"{k}: {v}")

print("\n=== EXECUTION DETAIL ===")
details = data.get("execution_detail", [])
print("Operation count:", len(details))

for i, item in enumerate(details):
    print(
        f"{i:03d} | "
        f"{item.get('name')} | "
        f"{item.get('type')} | "
        f"{item.get('compute_unit')} | "
        f"time={item.get('execution_time')} | "
        f"cycles={item.get('execution_cycles')}"
    )

print("\n=== COMPUTE UNIT COUNTS ===")
from collections import Counter
print(Counter(x.get("compute_unit") for x in details))

print("\n=== EXPLICIT UTILIZATION FIELDS ===")
for k, v in data.items():
    if "util" in k.lower() or "occup" in k.lower():
        print(k, ":", v)
