import json
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

MODEL_PATH = (
    ROOT
    / "models"
    / "edgeresilience"
    / "temporal_predictor_v4.pt"
)

ONNX_PATH = (
    ROOT
    / "models"
    / "edgeresilience"
    / "temporal_predictor_v4.onnx"
)

DATASET = (
    ROOT
    / "data"
    / "processed"
    / "temporal"
    / "edgeresilience_temporal_dataset_v4.jsonl"
)

records = [
    json.loads(line)
    for line in DATASET.open(
        "r",
        encoding="utf-8",
    )
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
        for record in records[:100]
    ],
    dtype=np.float32,
)

mean = X.mean(
    axis=(0, 1),
    keepdims=True,
)

std = X.std(
    axis=(0, 1),
    keepdims=True,
)

std = np.maximum(
    std,
    1e-6,
)

X = (
    X - mean
) / std

config = TemporalModelConfig(
    input_features=17,
    sequence_length=12,
    d_model=64,
    nhead=4,
    num_layers=2,
    dim_feedforward=128,
    dropout=0.10,
)

model = EdgeResilienceTemporalPredictor(
    config
)

checkpoint = torch.load(
    MODEL_PATH,
    map_location="cpu",
)

if (
    isinstance(checkpoint, dict)
    and "model_state_dict" in checkpoint
):
    state = checkpoint[
        "model_state_dict"
    ]
else:
    state = checkpoint

model.load_state_dict(state)
model.eval()

session = ort.InferenceSession(
    str(ONNX_PATH),
    providers=[
        "CPUExecutionProvider"
    ],
)

onnx_input_name = (
    session.get_inputs()[0].name
)

torch_predictions = []
onnx_predictions = []

with torch.no_grad():

    for sample in X:

        sample_batch = (
            torch.from_numpy(
                sample[None, :, :]
            )
        )

        torch_pred = (
            model(
                sample_batch
            )
            .numpy()
            .reshape(-1)[0]
        )

        onnx_pred = (
            session.run(
                None,
                {
                    onnx_input_name:
                    sample[None, :, :]
                },
            )[0]
            .reshape(-1)[0]
        )

        torch_predictions.append(
            float(torch_pred)
        )

        onnx_predictions.append(
            float(onnx_pred)
        )

torch_predictions = np.asarray(
    torch_predictions,
    dtype=np.float32,
)

onnx_predictions = np.asarray(
    onnx_predictions,
    dtype=np.float32,
)

absolute_error = np.abs(
    torch_predictions
    - onnx_predictions
)

max_abs_error = float(
    absolute_error.max()
)

mean_abs_error = float(
    absolute_error.mean()
)

rmse = float(
    np.sqrt(
        np.mean(
            (
                torch_predictions
                - onnx_predictions
            ) ** 2
        )
    )
)

passed = (
    max_abs_error < 1e-4
    and mean_abs_error < 1e-5
)

report = {
    "experiment":
        "V4 PyTorch ONNX numerical equivalence",

    "status":
        "PASS" if passed else "FAIL",

    "samples":
        len(X),

    "input_shape":
        [1, 12, 17],

    "max_absolute_error":
        max_abs_error,

    "mean_absolute_error":
        mean_abs_error,

    "rmse":
        rmse,

    "tolerance_max_absolute_error":
        1e-4,

    "tolerance_mean_absolute_error":
        1e-5,

    "onnx_input_shape":
        [1, 12, 17],

    "onnxruntime_provider":
        "CPUExecutionProvider",

    "snapdragon_hardware_verified":
        False,

    "qualcomm_qnn_verified":
        False,
}

output = (
    ROOT
    / "experiments"
    / "v4_onnx_equivalence_report.json"
)

output.write_text(
    json.dumps(
        report,
        indent=2,
    ),
    encoding="utf-8",
)

print("=" * 80)
print(
    "EDGERESILIENCE V4 "
    "ONNX NUMERICAL EQUIVALENCE"
)
print("=" * 80)
print(
    f"Samples             : {len(X)}"
)
print(
    f"Input shape         : {list(X.shape)}"
)
print(
    f"ONNX input shape    : [1, 12, 17]"
)
print(
    f"Max absolute error  : "
    f"{max_abs_error:.10f}"
)
print(
    f"Mean absolute error : "
    f"{mean_abs_error:.10f}"
)
print(
    f"RMSE                : "
    f"{rmse:.10f}"
)
print(
    "Equivalence         : "
    + ("PASS" if passed else "FAIL")
)
print(
    "Snapdragon hardware : FALSE"
)
print(
    "Qualcomm QNN        : FALSE"
)
print(
    "V4_ONNX_EQUIVALENCE = "
    + ("PASS" if passed else "FAIL")
)
