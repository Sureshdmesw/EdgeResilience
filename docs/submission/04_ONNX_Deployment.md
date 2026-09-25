# EdgeResilience — 04: ONNX Deployment

## Why ONNX Matters for Snapdragon

ONNX is the standard interchange format for deploying AI models
to Qualcomm's toolchain. The path from EdgeResilience to Snapdragon
NPU execution runs through ONNX:

```
PyTorch checkpoint (validated)
        │
        ▼
ONNX export (validated — dynamic batch)
        │
        ▼
Qualcomm QNN / HTP compilation
        │
        ▼
Snapdragon X Elite validated workload execution
        │
        ▼
HTP profiling completed
```

The ONNX export and CPU numerical equivalence remain validated.
Qualcomm QNN / HTP execution has subsequently been verified on a
Snapdragon X Elite CRD for selected V4 components and the temporal
pooling + prediction-head workload. Full production-model numerical
equivalence against the CPU reference remains unverified.

---

## ONNX Artifacts

| Artifact | Shape | Status |
|---|---|---|
| temporal_predictor_v4.onnx | [1, 12, 17] → [1] | VALIDATED |
| temporal_predictor_v4_dynamic.onnx | [batch, 12, 17] → [batch] | VALIDATED |

Dynamic ONNX SHA256: acb43a20c9fa64577c56bdfe3aa3c2ea96b6691420c0a7994dc5fd9f230c0e5d

---

## Numerical Equivalence

**Source:** experiments/v4_dynamic_onnx_equivalence_report.json

Dynamic ONNX vs PyTorch reference, threshold 1e-5:

| Batch size | Max absolute error | Result |
|---|---|---|
| 1 | 4.38e-08 | PASS |
| 4 | 3.54e-08 | PASS |
| 16 | 5.96e-08 | PASS |

Maximum error across all batches: **5.96e-08**
Threshold: 1e-05
Margin: **168× below threshold**

The ONNX model is numerically equivalent to the PyTorch reference.

---

## CPU Performance Evidence

**Source:** experiments/v4_pytorch_vs_onnx_cpu_benchmark.json
**Hardware:** Intel Core i5-1235U (Windows)

| Backend | Mean latency | Median latency | P95 latency |
|---|---|---|---|
| PyTorch (CPU) | 1.570 ms | 1.254 ms | 4.558 ms |
| ONNX Runtime (CPU) | 0.267 ms | 0.252 ms | 0.331 ms |
| Speedup (mean) | **~5.88×** | — | — |

**This is a CPU-to-CPU measurement on an Intel processor.**
**This is NOT a Snapdragon result.**
**This is NOT an NPU result.**

It demonstrates that ONNX Runtime deployment provides meaningful
efficiency improvement even before reaching the NPU — and that the
model is well-suited for further acceleration on Snapdragon.

---

## CPU Throughput Reference

**Source:** experiments/cpu_reference_benchmark_v4.json

| Metric | Value |
|---|---|
| Input shape | [1000, 12, 17] |
| Throughput | 33,800 samples/sec |
| Mean batch latency | 29.59 ms |

---

## Deployment Status Summary

| Backend | Status | Notes |
|---|---|---|
| CPU reference (PyTorch) | VERIFIED | Intel Core i5-1235U |
| ONNX Runtime (CPU) | VERIFIED | ~5.88× vs PyTorch, CPU-to-CPU |
| Qualcomm QNN / HTP | VERIFIED — COMPONENT / WORKLOAD | Snapdragon X Elite CRD |
| Snapdragon X Elite | VERIFIED — COMPONENT / WORKLOAD | Validated V4 workload |
| HTP profiling | VERIFIED | AI Hub: 6.876 ms estimated inference; NPU / HTP execution |
| Full CPU ↔ Snapdragon numerical equivalence | NOT VERIFIED | Current investigation |

Overall: **CPU_ONNX_VERIFIED_SNAPDRAGON_COMPONENT_WORKLOAD_VERIFIED**

Source: experiments/snapdragon_deployment_manifest_v4.json
