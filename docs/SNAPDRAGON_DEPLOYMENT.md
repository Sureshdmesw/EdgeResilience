# EdgeResilience — Snapdragon Deployment Documentation

**Status:** CPU_ONNX_VERIFIED_SNAPDRAGON_COMPONENT_WORKLOAD_VERIFIED
**Deployment Validation:** See docs/snapdragon/SNAPDRAGON_VALIDATION_REPORT.md

---

## Summary

The EdgeResilience V4 temporal predictor has been validated on CPU and
exported to ONNX. A QNN-ready ONNX derivative has been prepared with
constant folding applied (Mod operator eliminated, 336→176 nodes, all
standard ONNX opset 17 operators). The derivative is numerically
equivalent to the source ONNX (max error = 0.0 over 200 samples).

The deployment path to Snapdragon NPU via Qualcomm QNN is fully prepared
but not yet hardware-verified. The current machine (Lenovo IdeaPad 3,
Intel i5-1235U) contains no Qualcomm SoC, no QNN SDK, and no
QNNExecutionProvider.

---

## Model Deployment Specification

| Property | Value |
|---|---|
| Model | EdgeResilience_V4_TemporalPredictor |
| Checkpoint | models/edgeresilience/temporal_predictor_v4.pt |
| ONNX (static) | models/edgeresilience/temporal_predictor_v4.onnx |
| ONNX (dynamic) | models/edgeresilience/temporal_predictor_v4_dynamic.onnx |
| QNN-ready derivative | models/edgeresilience/snapdragon/temporal_predictor_v4_qnn_ready.onnx |
| Input shape | [batch, 12, 17] |
| Output shape | [batch] |
| Input dtype | float32 |
| Output dtype | float32 |
| Parameters | 71,170 |

---

## CPU Reference — VERIFIED

| Metric | Value |
|---|---|
| Hardware | Intel Core i5-1235U |
| OS | Windows |
| Framework | PyTorch 2.12.1+cpu |
| Input shape | [1000, 12, 17] |
| Mean batch latency | 29.59 ms |
| Median batch latency | 29.29 ms |
| P95 batch latency | 34.92 ms |
| Throughput | 33,800 samples/sec |

Source: experiments/cpu_reference_benchmark_v4.json

---

## ONNX Runtime CPU — VERIFIED

| Metric | Value |
|---|---|
| Hardware | Intel Core i5-1235U |
| OS | Windows |
| ONNX Runtime | 1.30.0 |
| Provider | CPUExecutionProvider |
| Input shape | [1, 12, 17] (batch-1 benchmark) |
| PyTorch mean latency | 1.570 ms |
| ONNX mean latency | 0.267 ms |
| ONNX median latency | 0.252 ms |
| ONNX P95 latency | 0.331 ms |
| Mean speedup vs PyTorch | ~5.88x |

**IMPORTANT:** This is a CPU-to-CPU measurement on an Intel processor.
This is NOT a Snapdragon result.
This is NOT an NPU result.
This is NOT a Qualcomm acceleration result.

Source: experiments/v4_pytorch_vs_onnx_cpu_benchmark.json

---

## Dynamic ONNX Numerical Equivalence — VERIFIED

| Batch size | Max absolute error | Threshold | Result |
|---|---|---|---|
| 1 | 4.38e-08 | 1e-05 | PASS |
| 4 | 3.54e-08 | 1e-05 | PASS |
| 16 | 5.96e-08 | 1e-05 | PASS |

Source: experiments/v4_dynamic_onnx_equivalence_report.json

---

## QNN-Ready Derivative — VERIFIED (Software)

| Property | Value |
|---|---|
| Source | models/edgeresilience/temporal_predictor_v4_dynamic.onnx |
| Source SHA256 | ACB43A20C9FA64577C56BDFE3AA3C2EA96B6691420C0A7994DC5FD9F230C0E5D |
| Derivative | models/edgeresilience/snapdragon/temporal_predictor_v4_qnn_ready.onnx |
| Derivative SHA256 | E2B22D8A872F1AFEF2CFD34FDE11295EC69F2BC3C4324402F284EC4F6422A62E |
| Provenance | ADAPTED via ORT_ENABLE_BASIC constant folding |
| Mod nodes eliminated | YES (2 → 0) |
| Node count | 176 (was 336) |
| Operators | All standard ONNX opset 17 — no ORT-internal fused ops |
| Unsupported QNN ops | NONE |
| ONNX checker | PASS |
| Numerical equivalence | PASS — max error = 0.0 (200 samples) |
| QNN execution | VERIFIED — Qualcomm QNN/HTP workload |

Source: experiments/snapdragon/qnn_ready_model_report.json

---

## Qualcomm QNN / HTP — COMPONENT / WORKLOAD VERIFIED

| Property | Status |
|---|---|
| Qualcomm QNN / HTP compilation | VERIFIED — Qualcomm AI Hub |
| Snapdragon X Elite target | VERIFIED |
| QNN / HTP execution | VERIFIED — validated workload |
| HTP profiling | VERIFIED |
| Full CPU ↔ Snapdragon numerical equivalence | NOT VERIFIED |

The current evidence was generated through Qualcomm AI Hub and the
Snapdragon X Elite CRD. The remaining validation work is:

1. Investigate operator-level CPU-to-Snapdragon numerical divergence.
2. Re-run the complete production-model comparison after corrective
   graph/operator changes.
3. Verify full-model numerical equivalence against the CPU reference
   using the established 1e-5 threshold.
4. Record any revised compile, inference, and profiling evidence.
5. Keep physical vehicle, external CAN, direct actuation, and
   production-vehicle validation outside the current evidence boundary.

---

## Snapdragon Hardware — COMPONENT / WORKLOAD VERIFIED

| Property | Status |
|---|---|
| Device | Snapdragon X Elite CRD |
| SoC | Qualcomm SC8380XP |
| Accelerator | Hexagon v73 / HTP |
| HTP execution | VERIFIED — validated workload |
| HTP utilization | 97.22% |
| Estimated inference time | 36 µs |
| Throughput | ~3,984 inferences/sec |
| Peak inference memory | ~27.83 MiB |
| Power consumption | NOT MEASURED |
| Thermal behavior | NOT MEASURED |
| Full CPU ↔ Snapdragon numerical equivalence | NOT VERIFIED |

The above Snapdragon measurements are workload-specific profiling results.
They are not claims of complete vehicle-system latency, power, or thermal
performance.

---

## Deployment Path

The intended deployment path is:

```
PyTorch checkpoint (VERIFIED)
        |
        v
ONNX export (VERIFIED — dynamic batch, max error 5.96e-8)
        |
        v
QNN-ready ONNX derivative (VERIFIED — Mod eliminated, max error 0.0)
        |
        v
Qualcomm AI Hub QNN / HTP compilation (VERIFIED)
        |
        v
Snapdragon X Elite CRD workload execution (VERIFIED)
        |
        v
HTP profiling (VERIFIED)
        |
        v
Full CPU ↔ Snapdragon numerical equivalence (NOT VERIFIED)
        |
        v
Vehicle deployment (NOT PERFORMED)
```

---

## What Would Be Measured on Snapdragon

If Snapdragon hardware and QNN SDK become available, the following should
be measured and documented:

1. Device identification (SoC model, firmware version)
2. SDK version (QNN SDK version, ONNX converter version)
3. Execution provider (CPU, HTP/NPU, GPU)
4. Batch-1 inference latency (mean, median, P95, P99)
5. Throughput (inferences per second)
6. Peak memory usage (MB)
7. Power consumption (watts) — if measurement API available
8. Thermal behavior — if measurement API available
9. Numerical equivalence vs CPU reference (threshold 1e-5)
10. Accuracy preservation (MAE/RMSE on V4 test set)

All measurements must be recorded with hardware and software version
information and stored as separate EdgeResilience evidence artifacts.

---

## Backend Status Summary

| Backend | Verified | Notes |
|---|---|---|
| CPU reference (PyTorch) | YES | Intel Core i5-1235U, 33,800 samples/sec |
| ONNX Runtime (CPU) | YES | CPUExecutionProvider, ~5.99x vs PyTorch |
| QNN-ready ONNX derivative | YES (software) | Mod eliminated, equiv PASS, awaits QNN SDK |
| Qualcomm QNN / HTP | YES — component/workload | Snapdragon X Elite CRD |
| Snapdragon X Elite | YES — component/workload | Qualcomm SC8380XP / HTP |
| Full CPU ↔ Snapdragon equivalence | NO | Operator-level investigation ongoing |
| GPU | NO | Not tested |

---

## Safety Note

Deployment verification does not change the safety boundary.
The system remains a software simulation / virtual laboratory regardless
of which inference backend is used.

Physical vehicle testing, external CAN transmission, and direct actuation
are not performed on any backend.
