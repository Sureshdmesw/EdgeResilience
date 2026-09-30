import json
import numpy as np
from pathlib import Path

p = Path(r"experiments\snapdragon\profile_artifacts\v4_full_production\EdgeResilience V4 QNN-Ready Full Model HTP Profile_jpxlwmxlp_results.json")

with p.open("r", encoding="utf-8") as f:
    data = json.load(f)

t = np.asarray(data["execution_summary"]["all_inference_times"], dtype=np.float64)

# QAI Hub timing values are microseconds.
warm = t[1:]  # exclude first cold inference
warm_s = warm / 1_000_000.0

print("=" * 80)
print("FULL PRODUCTION V4 THROUGHPUT ANALYSIS")
print("=" * 80)

print("Total inference samples:", len(t))
print("Cold sample (us):", t[0])

print("\n=== ALL SAMPLES ===")
print("Mean (us):", np.mean(t))
print("Median (us):", np.median(t))
print("Min (us):", np.min(t))
print("Max (us):", np.max(t))

print("\n=== WARM SAMPLES ===")
print("Samples:", len(warm))
print("Mean (us):", np.mean(warm))
print("Median (us):", np.median(warm))
print("P50 (us):", np.percentile(warm, 50))
print("P90 (us):", np.percentile(warm, 90))
print("P95 (us):", np.percentile(warm, 95))
print("P99 (us):", np.percentile(warm, 99))
print("Min (us):", np.min(warm))
print("Max (us):", np.max(warm))

print("\n=== THROUGHPUT ESTIMATES ===")
print("Using profile estimated latency 63 us:")
print("Theoretical rate (inferences/sec):", 1_000_000.0 / 63.0)

mean_us = np.mean(warm)
median_us = np.median(warm)

print("Warm mean rate (inferences/sec):", 1_000_000.0 / mean_us)
print("Warm median rate (inferences/sec):", 1_000_000.0 / median_us)

print("\n=== PROFILE INTERPRETATION ===")
print("These are single-batch profile timings, not a separately measured sustained throughput benchmark.")
