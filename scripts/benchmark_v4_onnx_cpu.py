import json
import time
from pathlib import Path
import sys

import numpy as np
import torch
import onnxruntime as ort

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.ai.temporal_predictor import (
    EdgeResilienceTemporalPredictor,
    TemporalModelConfig,
)

MODEL_PATH = ROOT / "models" / "edgeresilience" / "temporal_predictor_v4.pt"
ONNX_PATH = ROOT / "models" / "edgeresilience" / "temporal_predictor_v4.onnx"
DATASET = ROOT / "data" / "processed" / "temporal" / "edgeresilience_temporal_dataset_v4.jsonl"

records = [
    json.loads(line)
    for line in DATASET.open("r", encoding="utf-8")
]

feature_names = list(records[0]["observations"][0].keys())

X = np.asarray(
    [
        [
            [obs[name] for name in feature_names]
            for obs in record["observations"]
        ]
        for record in records[:100]
    ],
    dtype=np.float32,
)

mean = X.mean(axis=(0, 1), keepdims=True)
std = np.maximum(
    X.std(axis=(0, 1), keepdims=True),
    1e-6,
)

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

state = (
    checkpoint["model_state_dict"]
    if isinstance(checkpoint, dict)
    and "model_state_dict" in checkpoint
    else checkpoint
)

model.load_state_dict(state)
model.eval()

session = ort.InferenceSession(
    str(ONNX_PATH),
    providers=["CPUExecutionProvider"],
)

input_name = session.get_inputs()[0].name

warmup = 20
runs = 100

torch_times = []
onnx_times = []

for sample in X:

    sample = sample[None, :, :]
    x_torch = torch.from_numpy(sample)

    for _ in range(warmup):
        with torch.no_grad():
            _ = model(x_torch)

    for _ in range(warmup):
        _ = session.run(
            None,
            {input_name: sample},
        )

    local_torch = []

    for _ in range(runs):
        start = time.perf_counter()

        with torch.no_grad():
            _ = model(x_torch)

        local_torch.append(
            (time.perf_counter() - start) * 1000.0
        )

    local_onnx = []

    for _ in range(runs):
        start = time.perf_counter()

        _ = session.run(
            None,
            {input_name: sample},
        )

        local_onnx.append(
            (time.perf_counter() - start) * 1000.0
        )

    torch_times.append(
        float(np.mean(local_torch))
    )

    onnx_times.append(
        float(np.mean(local_onnx))
    )

torch_times = np.asarray(torch_times)
onnx_times = np.asarray(onnx_times)

torch_mean = float(torch_times.mean())
torch_median = float(np.median(torch_times))
torch_p95 = float(np.percentile(torch_times, 95))

onnx_mean = float(onnx_times.mean())
onnx_median = float(np.median(onnx_times))
onnx_p95 = float(np.percentile(onnx_times, 95))

speedup = torch_mean / onnx_mean

result = {
    "experiment": "V4 PyTorch vs ONNX Runtime CPU batch-1 benchmark",
    "status": "PASS",
    "samples": len(X),
    "warmup_runs_per_sample": warmup,
    "benchmark_runs_per_sample": runs,
    "input_shape": [1, 12, 17],
    "pytorch": {
        "mean_latency_ms": torch_mean,
        "median_latency_ms": torch_median,
        "p95_latency_ms": torch_p95,
    },
    "onnxruntime_cpu": {
        "mean_latency_ms": onnx_mean,
        "median_latency_ms": onnx_median,
        "p95_latency_ms": onnx_p95,
    },
    "onnx_mean_latency_speedup": speedup,
    "hardware_verified": False,
    "accelerator_verified": False,
    "notes": (
        "Batch-1 CPU reference/interoperability benchmark. "
        "No Snapdragon or Qualcomm accelerator performance "
        "is claimed."
    ),
}

output = (
    ROOT
    / "experiments"
    / "v4_pytorch_vs_onnx_cpu_benchmark.json"
)

output.write_text(
    json.dumps(result, indent=2),
    encoding="utf-8",
)

print("=" * 80)
print("EDGERESILIENCE V4 PYTORCH VS ONNX RUNTIME CPU")
print("=" * 80)
print("Input shape          : [1, 12, 17]")
print(f"Samples              : {len(X)}")
print()
print("PyTorch")
print(f"  Mean               : {torch_mean:.4f} ms")
print(f"  Median             : {torch_median:.4f} ms")
print(f"  P95                : {torch_p95:.4f} ms")
print()
print("ONNX Runtime CPU")
print(f"  Mean               : {onnx_mean:.4f} ms")
print(f"  Median             : {onnx_median:.4f} ms")
print(f"  P95                : {onnx_p95:.4f} ms")
print()
print(f"Mean latency ratio   : {speedup:.3f}x")
print("Snapdragon verified  : FALSE")
print("Qualcomm accelerator : FALSE")
print("V4_ONNX_CPU_BENCHMARK = PASS")
