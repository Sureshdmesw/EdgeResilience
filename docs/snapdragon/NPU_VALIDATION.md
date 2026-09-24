# EdgeResilience — NPU Validation

**Phase:** PHASE_7_NPU_SPECIFIC_EXECUTION
**Status:** NOT PERFORMED — no Snapdragon hardware present
**NPU Status:** NOT VERIFIED

---

## NPU Discovery

| Check | Result |
|---|---|
| Snapdragon NPU present | NOT PRESENT |
| Hexagon DSP present | NOT PRESENT |
| Qualcomm AI Engine Direct | NOT INSTALLED |
| QNN HTP backend | NOT VERIFIED |
| NPU execution provider | NOT PRESENT |

---

## Why NPU Status Cannot Be Claimed

NPU execution requires demonstrable routing to the Qualcomm Hexagon NPU/HTP backend.

The following are **NOT** sufficient evidence of NPU execution:

- Low inference latency
- Qualcomm device presence
- QNN SDK installation alone
- ONNX model compatibility
- Windows AI APIs (DirectML, WinML) — these are not Qualcomm NPU backends

NPU verification requires:

1. Snapdragon device with Hexagon NPU (e.g., Snapdragon X Elite HTP v75, Snapdragon 8cx Gen 3 HTP v68)
2. QNN SDK with HTP backend libraries (`QnnHtp.dll` / `libQnnHtp.so`)
3. Model compiled with `--use_htp` flag targeting the specific HTP version
4. Inference session explicitly using the HTP/NPU backend
5. Runtime confirmation that execution was routed to NPU (not CPU fallback)
6. Measured latency, throughput, and optionally power/thermal

---

## NPU Execution Procedure (Prepared — Requires Hardware)

When a Snapdragon device is available:

```bash
# Step 1: Convert to QNN with HTP target
qnn-onnx-converter \
  --input_network models/edgeresilience/snapdragon/temporal_predictor_v4_qnn_ready.onnx \
  --output_path models/edgeresilience/snapdragon/temporal_predictor_v4_htp.cpp \
  --input_dim vehicle_temporal_features 1,12,17 \
  --use_htp

# Step 2: Compile for target HTP version
qnn-model-lib-generator \
  -c models/edgeresilience/snapdragon/temporal_predictor_v4_htp.cpp \
  -b models/edgeresilience/snapdragon/temporal_predictor_v4_htp.bin \
  -t aarch64-android

# Step 3: Run inference via QNN runtime
python scripts/snapdragon_npu_validation.py \
  --model models/edgeresilience/snapdragon/temporal_predictor_v4_htp.bin \
  --backend QnnHtp \
  --iterations 1000 \
  --warmup 50
```

**REQUIRES SNAPDRAGON HARDWARE — cannot run on current machine.**

---

## Evidence Artifact

`experiments/snapdragon/npu_validation_report.json`

This file will be created when NPU execution is performed on actual hardware.
Current status: **NOT CREATED — hardware not available.**
