import json
import sys
from pathlib import Path

import numpy as np
import onnxruntime as ort
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.ai.temporal_predictor import (
    EdgeResilienceTemporalPredictor,
    TemporalModelConfig,
)

MODEL_PATH = ROOT / "models" / "edgeresilience" / "temporal_predictor_v4.pt"
ONNX_PATH = ROOT / "models" / "edgeresilience" / "temporal_predictor_v4_dynamic.onnx"
REPORT_PATH = ROOT / "experiments" / "v4_dynamic_onnx_equivalence_report.json"

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
checkpoint = torch.load(MODEL_PATH, map_location="cpu")

state = (
    checkpoint["model_state_dict"]
    if isinstance(checkpoint, dict)
    and "model_state_dict" in checkpoint
    else checkpoint
)

model.load_state_dict(state)
model.eval()

rng = np.random.default_rng(42)

# Test both batch=1 and batch>1.
inputs = [
    rng.standard_normal((1, 12, 17)).astype(np.float32),
    rng.standard_normal((4, 12, 17)).astype(np.float32),
    rng.standard_normal((16, 12, 17)).astype(np.float32),
]

session = ort.InferenceSession(
    str(ONNX_PATH),
    providers=["CPUExecutionProvider"],
)

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

results = []

with torch.no_grad():
    for x in inputs:
        torch_output = model(torch.from_numpy(x)).numpy()
        onnx_output = session.run(
            [output_name],
            {input_name: x},
        )[0]

        diff = np.abs(torch_output - onnx_output)

        results.append({
            "batch_size": int(x.shape[0]),
            "max_absolute_error": float(diff.max()),
            "mean_absolute_error": float(diff.mean()),
            "rmse": float(np.sqrt(np.mean(diff ** 2))),
        })

max_error = max(r["max_absolute_error"] for r in results)
passed = max_error < 1e-5

report = {
    "artifact": "temporal_predictor_v4_dynamic.onnx",
    "input_shape": ["batch", 12, 17],
    "output_shape": ["batch"],
    "provider": "CPUExecutionProvider",
    "batch_tests": results,
    "max_absolute_error": max_error,
    "equivalence_threshold": 1e-5,
    "equivalence_status": "PASS" if passed else "FAIL",
    "snapdragon_hardware_verified": False,
    "qualcomm_qnn_verified": False,
}

REPORT_PATH.write_text(
    json.dumps(report, indent=2),
    encoding="utf-8",
)

print("=" * 80)
print("EDGERESILIENCE V4 DYNAMIC ONNX NUMERICAL EQUIVALENCE")
print("=" * 80)

for r in results:
    print(
        f"batch={r['batch_size']:>2} | "
        f"max_abs={r['max_absolute_error']:.10f} | "
        f"mean_abs={r['mean_absolute_error']:.10f} | "
        f"RMSE={r['rmse']:.10f}"
    )

print("-" * 80)
print(f"Maximum absolute error: {max_error:.10f}")
print(f"Equivalence threshold:  {1e-5:.10f}")
print(f"RESULT: {'PASS' if passed else 'FAIL'}")
print("Snapdragon hardware verified: FALSE")
print("QUALCOMM_QNN_VERIFIED = FALSE")
