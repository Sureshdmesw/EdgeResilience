# EdgeResilience — Snapdragon Deployment Validation Report

**Project:** EdgeResilience: Snapdragon-Powered Predictive Intelligence for Connected Vehicle Safety
**Competition:** Qualcomm Snapdragon AI Lab Build and Present Challenge
**Report Type:** Snapdragon Deployment Validation
**Overall Status:** CPU_AND_ONNX_VALIDATED_SNAPDRAGON_PENDING

---

## 1. Objective

Determine whether Snapdragon hardware, Qualcomm QNN, and NPU execution can be verified in the current environment. If not, document the exact blocker, prepare all deployment artifacts, and establish a reproducible validation procedure for when the correct hardware is available.

---

## 2. Target Platform

| Field | Value |
|---|---|
| Intended target | Qualcomm Snapdragon X Elite / Snapdragon 8cx Gen 3 (or equivalent) |
| Target OS | Windows on ARM64 or Android |
| Target runtime | Qualcomm AI Engine Direct (QNN SDK 2.x) |
| Target backend | QNN HTP (Hexagon Tensor Processor) for NPU; QNN CPU as fallback |
| Current machine | Lenovo IdeaPad 3 15IAU7 — Intel i5-1235U — NOT a Snapdragon device |

---

## 3. Hardware

| Field | Value | Verified |
|---|---|---|
| Device | Lenovo IdeaPad 3 15IAU7 (82RK) | YES |
| SoC | Intel i5-1235U (12th Gen, Alder Lake) | YES |
| CPU | Intel Core i5-1235U, 10 cores, 12 threads | YES |
| GPU | Intel UHD Graphics | YES |
| NPU | NOT PRESENT | YES |
| Snapdragon SoC | NOT PRESENT | YES |
| Qualcomm hardware | NOT PRESENT | YES |
| Hexagon DSP | NOT PRESENT | YES |

---

## 4. Software Environment

| Component | Value | Verified |
|---|---|---|
| OS | Windows 10 (10.0.26200) | YES |
| Python | 3.11.9 | YES |
| PyTorch | 2.12.1+cpu | YES |
| ONNX | 1.23.0 | YES |
| ONNX Runtime | 1.30.0 | YES |
| ORT Providers | CPUExecutionProvider, AzureExecutionProvider | YES |
| QNNExecutionProvider | NOT PRESENT | YES |
| QNN SDK | NOT INSTALLED | YES |
| Qualcomm Python packages | NONE INSTALLED | YES |

---

## 5. Model

| Property | Value |
|---|---|
| Name | EdgeResilience_V4_TemporalPredictor |
| Architecture | Temporal Transformer |
| Input | vehicle_temporal_features: [batch, 12, 17] |
| Output | future_resilience_degradation: [batch] |
| d_model | 64 |
| Attention heads | 4 |
| Transformer layers | 2 |
| Feed-forward dim | 128 |
| Parameters | 71,170 |
| Test MAE | ~0.0051 |
| Test RMSE | ~0.0066 |

---

## 6. Model Provenance

| Artifact | Path | SHA256 | Integrity |
|---|---|---|---|
| PyTorch checkpoint | models/edgeresilience/temporal_predictor_v4.pt | B551AD9F...D26B9 | PASS |
| Dynamic ONNX | models/edgeresilience/temporal_predictor_v4_dynamic.onnx | ACB43A20...C0E5D | PASS |
| QNN-ready derivative | models/edgeresilience/snapdragon/temporal_predictor_v4_qnn_ready.onnx | E2B22D8A...62E | PASS |

Protected artifacts (checkpoint + source ONNX) were NOT modified.

---

## 7. ONNX Provenance

| Property | Value |
|---|---|
| IR version | 8 |
| Opset | ai.onnx 17 |
| Nodes | 336 |
| Operators | Add, Cast, Concat, Constant, Div, Erf, Gather, Gemm, LayerNormalization, MatMul, Mod, Mul, ReduceSum, Relu, Reshape, Shape, Sigmoid, Slice, Softmax, Sqrt, Squeeze, Transpose, Unsqueeze |
| External data | None |
| ONNX checker | PASS |
| ORT CPU inference | PASS |

---

## 8. QNN

| Item | Status |
|---|---|
| QNN SDK installed | NOT VERIFIED |
| QNN runtime available | NOT VERIFIED |
| QNNExecutionProvider in ORT | NOT VERIFIED |
| QNN CPU backend | NOT VERIFIED |
| QNN GPU backend | NOT VERIFIED |
| QNN HTP/NPU backend | NOT VERIFIED |
| QNN conversion performed | NOT PERFORMED |
| Blocker | No Snapdragon hardware. No QNN SDK. No QNN ORT provider. |

---

## 9. NPU

| Item | Status |
|---|---|
| Snapdragon NPU present | NOT PRESENT |
| Hexagon HTP available | NOT VERIFIED |
| NPU execution performed | NOT PERFORMED |
| NPU backend confirmed | NOT VERIFIED |
| NPU status | NOT VERIFIED |

---

## 10. Conversion

### Source ONNX → QNN-Ready Derivative

| Step | Result |
|---|---|
| Source integrity check | PASS |
| Mod operator analysis | Both Mod nodes operate on Constant inputs only (constant-foldable) |
| ORT_ENABLE_BASIC optimization | PASS — Mod eliminated, 336→176 nodes |
| Derivative ONNX checker | PASS |
| Derivative operators | All standard ONNX opset 17, no ORT-internal fused ops |
| Unsupported QNN operators | NONE |
| Numerical equivalence (200 samples) | PASS — max error = 0.0 |

### QNN SDK Conversion (qnn-onnx-converter)

| Step | Result |
|---|---|
| QNN SDK available | NOT VERIFIED |
| Conversion command prepared | YES |
| Conversion executed | NOT PERFORMED |
| QNN artifact produced | NOT PERFORMED |

---

## 11. Execution

| Backend | Status |
|---|---|
| CPU PyTorch | VERIFIED — 33,800 samples/sec, mean 1.66ms |
| ONNX CPU | VERIFIED — mean 0.28ms, ~5.99x vs PyTorch |
| Snapdragon CPU (QNN) | NOT VERIFIED |
| Snapdragon GPU (QNN) | NOT VERIFIED |
| Snapdragon NPU (QNN HTP) | NOT VERIFIED |

---

## 12. Numerical Equivalence

| Comparison | Max Error | Result |
|---|---|---|
| PyTorch vs ONNX CPU (dynamic) | 5.96e-8 | PASS |
| ONNX CPU vs QNN-ready derivative | 0.0 | PASS |
| QNN execution vs reference | NOT VERIFIED | — |

---

## 13. Performance

| Backend | Mean Latency | Median Latency | P95 Latency | Throughput |
|---|---|---|---|---|
| CPU PyTorch | 1.66ms | 1.62ms | 1.96ms | 33,800 samples/sec |
| ONNX CPU | 0.28ms | 0.28ms | 0.29ms | — |
| Snapdragon CPU | NOT VERIFIED | NOT VERIFIED | NOT VERIFIED | NOT VERIFIED |
| Snapdragon GPU | NOT VERIFIED | NOT VERIFIED | NOT VERIFIED | NOT VERIFIED |
| Snapdragon NPU | NOT VERIFIED | NOT VERIFIED | NOT VERIFIED | NOT VERIFIED |

Note: CPU benchmarks measured on Intel Core i5-1235U. These are NOT Snapdragon results.

---

## 14. Resource Measurements

| Metric | Value |
|---|---|
| Source ONNX model size | See experiments/snapdragon/snapdragon_deployment_manifest.json |
| QNN-ready derivative size | See experiments/snapdragon/snapdragon_deployment_manifest.json |
| Memory footprint (Snapdragon) | NOT VERIFIED |
| Power (Snapdragon) | NOT VERIFIED |
| Thermal (Snapdragon) | NOT VERIFIED |
| Runtime init time (Snapdragon) | NOT VERIFIED |

---

## 15. Limitations

1. No Snapdragon hardware available — all Snapdragon/QNN/NPU claims remain NOT VERIFIED
2. QNN conversion not performed — no QNN SDK installed
3. CPU benchmarks are Intel i5-1235U measurements, not Snapdragon measurements
4. ONNX speedup (~5.99x) is CPU-to-CPU on Intel hardware, not NPU acceleration
5. QNN compatibility assessment is theoretical — based on operator set analysis only
6. LayerNormalization HTP support requires QNN SDK >= 2.10 (version-dependent)

---

## 16. Safety Boundary

This is a software simulation / virtual laboratory.

- Physical vehicle test: NO
- External CAN transmission: NO
- Direct actuation: NO
- Production vehicle connection: NO
- Real emergency dispatch: NO

Snapdragon deployment validation is software inference validation only.

---

## 17. Reproducibility

See `docs/snapdragon/REPRODUCE_SNAPDRAGON.md` for exact reproduction commands.

Steps executable on current machine:
- Environment discovery: `python scripts/snapdragon_environment_discovery.py`
- QNN discovery: `python scripts/snapdragon_qnn_discovery.py`
- Model compatibility: `python scripts/snapdragon_model_compatibility.py`
- QNN-ready derivative: `python scripts/snapdragon_prepare_qnn_ready_model.py`
- Deployment manifest: `python scripts/snapdragon_deployment_manifest.py`

Steps requiring Snapdragon hardware:
- QNN conversion, QNN execution, NPU execution, performance benchmarking

---

## 18. Final Verification Status

| Capability | Status |
|---|---|
| CPU reference (PyTorch) | VERIFIED |
| ONNX Runtime (CPU) | VERIFIED |
| ONNX numerical equivalence | VERIFIED |
| QNN-ready derivative prepared | VERIFIED |
| QNN-ready derivative equivalence | VERIFIED |
| Snapdragon hardware | NOT VERIFIED |
| Qualcomm QNN | NOT VERIFIED |
| QNN conversion | NOT VERIFIED |
| Snapdragon execution | NOT VERIFIED |
| NPU execution | NOT VERIFIED |
| Snapdragon latency | NOT VERIFIED |
| Snapdragon throughput | NOT VERIFIED |
| Snapdragon memory | NOT VERIFIED |
| Snapdragon power | NOT VERIFIED |
| Snapdragon thermal | NOT VERIFIED |
