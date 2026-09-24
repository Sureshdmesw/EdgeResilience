import json
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.ai.temporal_predictor import (
    EdgeResilienceTemporalPredictor,
    TemporalModelConfig,
)

MODEL_PATH = ROOT / "models" / "edgeresilience" / "temporal_predictor_v4.pt"
OUTPUT = ROOT / "models" / "edgeresilience" / "temporal_predictor_v4_dynamic.onnx"
REPORT = ROOT / "experiments" / "v4_dynamic_onnx_export_report.json"

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

dummy = torch.randn(1, 12, 17)

torch.onnx.export(
    model,
    dummy,
    OUTPUT,
    input_names=["vehicle_temporal_features"],
    output_names=["future_resilience_degradation"],
    dynamic_axes={
        "vehicle_temporal_features": {
            0: "batch"
        },
        "future_resilience_degradation": {
            0: "batch"
        },
    },
    opset_version=17,
    dynamo=False,
)

report = {
    "artifact": "temporal_predictor_v4_dynamic.onnx",
    "source_model": "temporal_predictor_v4.pt",
    "input_shape": ["batch", 12, 17],
    "output_shape": ["batch"],
    "opset": 17,
    "dynamo": False,
    "dynamic_batch_requested": True,
    "export_status": "PASS",
    "dynamic_batch_equivalence": "PENDING",
    "snapdragon_hardware_verified": False,
    "qualcomm_qnn_verified": False,
}

REPORT.write_text(
    json.dumps(report, indent=2),
    encoding="utf-8",
)

print("=" * 80)
print("EDGERESILIENCE V4 DYNAMIC ONNX RE-EXPORT")
print("=" * 80)
print(f"Created: {OUTPUT}")
print(f"Size: {OUTPUT.stat().st_size / 1024 / 1024:.4f} MB")
print("Exporter: torch.onnx.export")
print("dynamo: FALSE")
print("Dynamic batch requested: TRUE")
print("Export: PASS")
print("Dynamic equivalence: PENDING")
print("Snapdragon hardware verified: FALSE")
print("QUALCOMM_QNN_VERIFIED = FALSE")
