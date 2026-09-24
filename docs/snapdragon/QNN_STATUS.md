# EdgeResilience — Qualcomm QNN Status

**Phase:** PHASE_3_QUALCOMM_QNN_DISCOVERY
**Status:** COMPLETE
**QNN Status:** NOT VERIFIED

---

## QNN Discovery Results

| Check | Result | Method |
|---|---|---|
| QNN Python packages | NONE INSTALLED | importlib probe for qai_hub, onnxruntime_qnn, qnn_wrapper, qualcomm_ai_engine_direct |
| QNN SDK directories | NONE FOUND | Filesystem scan of C:\Program Files\Qualcomm, C:\QNN, C:\QAIRT |
| QNN environment variables | NONE SET | Env var scan for QNN_SDK_ROOT, HEXAGON_SDK_ROOT, QAIRT_SDK_ROOT |
| QNN DLLs in System32 | NONE FOUND | Scan for QnnCpu.dll, QnnGpu.dll, QnnHtp.dll, QnnSystem.dll |
| QNNExecutionProvider in ORT | NOT PRESENT | onnxruntime.get_available_providers() |
| Qualcomm hardware | NOT PRESENT | PnP device scan |

---

## QNN Backend Status

| Backend | Status |
|---|---|
| QNN CPU backend | NOT VERIFIED |
| QNN GPU backend | NOT VERIFIED |
| QNN HTP/NPU backend | NOT VERIFIED |
| QNN runtime initialization | NOT VERIFIED |

---

## Important Distinctions

The following are **NOT** evidence of QNN execution:

- `CPUExecutionProvider` in ONNX Runtime — this is Intel/AMD CPU execution, not Qualcomm
- `AzureExecutionProvider` — this is Azure cloud inference, not Qualcomm
- ONNX model existence — a model file is not evidence of QNN execution
- Low inference latency — fast CPU inference is not NPU execution
- Qualcomm package names in pip — no Qualcomm packages are installed

---

## What QNN Verification Requires

1. Snapdragon-equipped device (hardware prerequisite)
2. Qualcomm AI Engine Direct SDK installed (`QNN_SDK_ROOT` set)
3. `qnn-onnx-converter` available on PATH
4. `QNNExecutionProvider` present in `onnxruntime.get_available_providers()`
5. Successful model conversion producing a `.bin` or `.cpp` QNN artifact
6. Successful inference session using `QNNExecutionProvider`
7. Numerical equivalence verified against PyTorch/ONNX CPU reference

---

## QNN Conversion Command (Prepared — Requires Hardware)

```
qnn-onnx-converter \
  --input_network models/edgeresilience/snapdragon/temporal_predictor_v4_qnn_ready.onnx \
  --output_path models/edgeresilience/snapdragon/temporal_predictor_v4.cpp \
  --input_dim vehicle_temporal_features 1,12,17
```

**REQUIRES SNAPDRAGON HARDWARE AND QNN SDK — cannot run on current machine.**

---

## Evidence Artifact

`experiments/snapdragon/qnn_environment_report.json`
