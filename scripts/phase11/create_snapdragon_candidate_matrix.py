from pathlib import Path
import csv

root = Path(r"E:\EdgeResilience")
out = root / "artifacts" / "phase11" / "snapdragon_aihub" / "candidate_matrix.csv"

headers = [
    "Model",
    "Domain",
    "Use Case",
    "Snapdragon X Elite Support",
    "Qualcomm Runtime",
    "NPU",
    "Precision",
    "Latency",
    "Memory",
    "Potential EdgeResilience Role",
    "AI Hub Evidence",
    "Integration Status"
]

with out.open("w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerow(headers)

print(out)
