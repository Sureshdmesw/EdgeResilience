# EdgeResilience — Snapdragon Validation Reproducibility

All commands run from project root: `E:\EdgeResilience`

---

## Steps Executable on Current Machine (Intel i5-1235U)

### 1. Environment Discovery

```
python scripts\snapdragon_environment_discovery.py
```

Output: `experiments/snapdragon/environment_report.json`

### 2. QNN Discovery

```
python scripts\snapdragon_qnn_discovery.py
```

Output: `experiments/snapdragon/qnn_environment_report.json`

### 3. Model Compatibility Analysis

```
python scripts\snapdragon_model_compatibility.py
```

Output: `experiments/snapdragon/model_compatibility_report.json`

### 4. QNN-Ready Derivative Preparation

```
python scripts\snapdragon_prepare_qnn_ready_model.py
```

Output: `models/edgeresilience/snapdragon/temporal_predictor_v4_qnn_ready.onnx`
Output: `experiments/snapdragon/qnn_ready_model_report.json`

### 5. Deployment Manifest

```
python scripts\snapdragon_deployment_manifest.py
```

Output: `experiments/snapdragon/snapdragon_deployment_manifest.json`

### 6. Protected Artifact Integrity

```
python _integrity_check.py
```

### 7. Full V4 Baseline Validation

```
python -m py_compile src\snapdragon\deployment.py
python -m py_compile src\ai\v4_inference.py
python -m py_compile src\resilience\v4_runtime.py
python -m py_compile src\dashboard\server.py
python -m py_compile demo\run_demo.py
python demo\run_demo.py
python scripts\generate_v4_demo_evidence.py
python scripts\validate_temporal_dataset_v4.py
python scripts\validate_v4_onnx_equivalence.py
python scripts\validate_v4_dynamic_onnx_equivalence.py
python scripts\benchmark_v4_onnx_cpu.py
```

---

## Steps Requiring Snapdragon Hardware

**REQUIRES SNAPDRAGON HARDWARE** — cannot run on current Intel machine.

### Prerequisites

- Device with Qualcomm Snapdragon SoC (Snapdragon X Elite, 8cx Gen 3, or equivalent)
- Qualcomm AI Engine Direct SDK (QNN SDK) >= 2.x installed
- `QNN_SDK_ROOT` environment variable set
- `qnn-onnx-converter` on PATH
- `onnxruntime-qnn` Python package installed

### QNN Conversion (CPU backend)

```bash
qnn-onnx-converter \
  --input_network models/edgeresilience/snapdragon/temporal_predictor_v4_qnn_ready.onnx \
  --output_path models/edgeresilience/snapdragon/temporal_predictor_v4.cpp \
  --input_dim vehicle_temporal_features 1,12,17
```

### QNN Conversion (HTP/NPU backend)

```bash
qnn-onnx-converter \
  --input_network models/edgeresilience/snapdragon/temporal_predictor_v4_qnn_ready.onnx \
  --output_path models/edgeresilience/snapdragon/temporal_predictor_v4_htp.cpp \
  --input_dim vehicle_temporal_features 1,12,17 \
  --use_htp
```

### QNN Model Library Compilation

```bash
qnn-model-lib-generator \
  -c models/edgeresilience/snapdragon/temporal_predictor_v4_htp.cpp \
  -b models/edgeresilience/snapdragon/temporal_predictor_v4_htp.bin \
  -t aarch64-android
```

### QNN Execution Validation

```bash
python scripts/snapdragon_npu_validation.py \
  --model models/edgeresilience/snapdragon/temporal_predictor_v4_htp.bin \
  --backend QnnHtp \
  --iterations 1000 \
  --warmup 50 \
  --reference_onnx models/edgeresilience/temporal_predictor_v4_dynamic.onnx
```

### QNN ORT Execution Provider Validation

```python
import onnxruntime as ort
import numpy as np

sess = ort.InferenceSession(
    "models/edgeresilience/snapdragon/temporal_predictor_v4_qnn_ready.onnx",
    providers=["QNNExecutionProvider"],
    provider_options=[{"backend_path": "QnnHtp.dll"}],
)
x = np.random.randn(1, 12, 17).astype(np.float32)
result = sess.run(None, {"vehicle_temporal_features": x})
print("QNN output:", result[0])
print("Providers:", sess.get_providers())
```

---

## Input Contract

All validation uses the same logical input:

- Shape: `[batch, 12, 17]`
- dtype: float32
- Semantics: 12 sequential temporal observations, 17 cyber-physical features each
- Input name: `vehicle_temporal_features`
- Output name: `future_resilience_degradation`

Do not change the input contract. Do not retrain the model.

---

## Expected Numerical Tolerance

| Comparison | Tolerance | Expected |
|---|---|---|
| PyTorch vs ONNX CPU | 1e-5 | < 1e-7 (actual: 5.96e-8) |
| ONNX CPU vs QNN-ready | 1e-5 | 0.0 (actual: 0.0) |
| QNN execution vs reference | 1e-4 | TBD on hardware |

If QNN numerical equivalence fails (max error > 1e-4), stop that deployment path and diagnose.
