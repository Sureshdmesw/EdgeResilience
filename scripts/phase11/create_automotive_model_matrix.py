from pathlib import Path
import csv

root = Path(r"E:\EdgeResilience")
out = root / "artifacts" / "phase11" / "qualcomm_automotive" / "automotive_model_matrix.csv"

rows = [
    ["Model", "Domain", "Automotive relevance", "Qualcomm device support",
     "Runtime", "NPU", "Precision", "Latency", "Memory",
     "EdgeResilience role", "Decision", "Evidence URL"],
]

out.parent.mkdir(parents=True, exist_ok=True)

with out.open("w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows)

print("Created:", out)
