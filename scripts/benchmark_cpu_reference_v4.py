import json
import time
from pathlib import Path
import sys

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.ai.temporal_predictor import (
    EdgeResilienceTemporalPredictor,
    TemporalModelConfig,
)

MODEL_PATH = (
    ROOT
    / "models"
    / "edgeresilience"
    / "temporal_predictor_v4.pt"
)

DATASET = (
    ROOT
    / "data"
    / "processed"
    / "temporal"
    / "edgeresilience_temporal_dataset_v4.jsonl"
)

torch.set_grad_enabled(False)

records = [
    json.loads(line)
    for line in DATASET.open("r", encoding="utf-8")
]

feature_names = list(
    records[0]["observations"][0].keys()
)

X = np.asarray(
    [
        [
            [obs[name] for name in feature_names]
            for obs in record["observations"]
        ]
        for record in records
    ],
    dtype=np.float32,
)

X = X[:1000]

mean = X.mean(
    axis=(0, 1),
    keepdims=True,
)

std = X.std(
    axis=(0, 1),
    keepdims=True,
)

std = np.maximum(std, 1e-6)

X = (X - mean) / std

config = TemporalModelConfig(
    input_features=17,
    sequence_length=12,
    d_model=64,
    nhead=4,
    num_layers=2,
    dim_feedforward=128,
    dropout=0.10,
)

model = EdgeResilienceTemporalPredictor(config)

checkpoint = torch.load(
    MODEL_PATH,
    map_location="cpu",
)

if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
    state = checkpoint["model_state_dict"]
else:
    state = checkpoint

model.load_state_dict(state)
model.eval()

x = torch.from_numpy(X)

warmup_runs = 20
benchmark_runs = 100

for _ in range(warmup_runs):
    _ = model(x)

times_ms = []

for _ in range(benchmark_runs):
    start = time.perf_counter()

    _ = model(x)

    elapsed = (
        time.perf_counter() - start
    ) * 1000.0

    times_ms.append(elapsed)

times_ms = np.asarray(times_ms)

mean_ms = float(times_ms.mean())
median_ms = float(np.median(times_ms))
p95_ms = float(np.percentile(times_ms, 95))

batch_size = len(x)

throughput = (
    batch_size / (mean_ms / 1000.0)
)

result = {
    "experiment": "EdgeResilience V4 CPU reference benchmark",
    "status": "PASS",
    "model": "temporal_predictor_v4",
    "model_format": "PyTorch",
    "device": "reference_cpu",
    "hardware_verified": False,
    "accelerator_verified": False,
    "dataset": "edgeresilience_temporal_dataset_v4.jsonl",
    "samples_per_run": batch_size,
    "warmup_runs": warmup_runs,
    "benchmark_runs": benchmark_runs,
    "mean_batch_latency_ms": mean_ms,
    "median_batch_latency_ms": median_ms,
    "p95_batch_latency_ms": p95_ms,
    "throughput_samples_per_second": throughput,
    "input_shape": [batch_size, 12, 17],
    "notes": (
        "CPU reference measurement only. "
        "No Snapdragon hardware or Qualcomm accelerator "
        "performance is claimed."
    ),
}

output = (
    ROOT
    / "experiments"
    / "cpu_reference_benchmark_v4.json"
)

output.write_text(
    json.dumps(
        result,
        indent=2,
    ),
    encoding="utf-8",
)

print("=" * 80)
print("EDGERESILIENCE V4 CPU REFERENCE BENCHMARK")
print("=" * 80)
print(f"Mean batch latency : {mean_ms:.4f} ms")
print(f"Median batch latency: {median_ms:.4f} ms")
print(f"P95 batch latency  : {p95_ms:.4f} ms")
print(f"Throughput         : {throughput:.2f} samples/sec")
print("Hardware verified  : FALSE")
print("Accelerator verified: FALSE")
print("CPU_REFERENCE_BENCHMARK_V4 = PASS")
