import json
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

OUTPUT = (
    ROOT
    / "models"
    / "edgeresilience"
    / "temporal_predictor_v4.onnx"
)

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

dummy_input = torch.randn(
    1,
    12,
    17,
    dtype=torch.float32,
)

torch.onnx.export(
    model,
    dummy_input,
    OUTPUT,
    input_names=["vehicle_temporal_features"],
    output_names=["future_resilience_degradation"],
    dynamic_axes=None,
    opset_version=17,
)

metadata = {
    "artifact": "temporal_predictor_v4.onnx",
    "source_model": "temporal_predictor_v4.pt",
    "input_shape": [1, 12, 17],
    "output_shape": [1],
    "opset": 17,
    "export_status": "PASS",
    "snapdragon_hardware_verified": False,
    "qualcomm_qnn_verified": False,
}

report = (
    ROOT
    / "experiments"
    / "v4_onnx_export_report.json"
)

report.write_text(
    json.dumps(
        metadata,
        indent=2,
    ),
    encoding="utf-8",
)

print("=" * 80)
print("EDGERESILIENCE V4 ONNX EXPORT")
print("=" * 80)
print(f"Created: {OUTPUT}")
print(f"Size: {OUTPUT.stat().st_size / 1024 / 1024:.2f} MB")
print("ONNX export: PASS")
print("Snapdragon hardware verified: FALSE")
print("QUALCOMM_QNN_VERIFIED = FALSE")
