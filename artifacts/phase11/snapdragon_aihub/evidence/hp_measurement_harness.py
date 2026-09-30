import csv
import os
import platform
import time
from datetime import datetime

OUT = r"artifacts\phase11\snapdragon_aihub\evidence\hp_snapdragon_measurements.csv"

os.makedirs(os.path.dirname(OUT), exist_ok=True)

row = {
    "timestamp": datetime.now().isoformat(),
    "platform": platform.platform(),
    "machine": platform.machine(),
    "processor": platform.processor(),
    "python": platform.python_version(),
    "inference_ms": "",
    "cpu_percent": "",
    "memory_mb": "",
    "npu_utilization_percent": "",
    "power_watts": "",
    "temperature_c": "",
    "notes": "Measurement harness initialized; hardware measurements not yet captured."
}

exists = os.path.exists(OUT)

with open(OUT, "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=row.keys())
    if not exists:
        writer.writeheader()
    writer.writerow(row)

print("HARNESS CREATED:", OUT)
print("Machine:", row["machine"])
print("Processor:", row["processor"])
