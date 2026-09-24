# EdgeResilience — 05: Snapdragon Optimization Path

## Design Intent

EdgeResilience is **designed for on-device deployment on
Snapdragon-powered HP PCs**.

The architecture, model size, ONNX export, and runtime design
are all deliberate choices made with Snapdragon edge deployment
as the target.

This document explains the intended optimization path and what
remains to be verified on actual hardware.

---

## Why EdgeResilience Is a Natural Snapdragon Workload

Qualcomm Snapdragon AI PCs include a dedicated NPU specifically
designed for always-on, low-latency AI inference. EdgeResilience
maps directly onto this capability:

| EdgeResilience requirement | Snapdragon capability |
|---|---|
| Always-on temporal inference | Dedicated NPU for continuous workloads |
| Low latency per inference | NPU hardware acceleration |
| No cloud dependency | On-device AI processing |
| Low power for edge deployment | Snapdragon power efficiency |
| Compact model (71K params) | Well-suited for NPU execution |
| ONNX deployment artifact | Standard QNN conversion input |

---

## Current Validated Position

```
TODAY — VALIDATED
─────────────────────────────────────────────────────────────
✓  V4 Temporal Transformer trained and validated
   MAE 0.0051 | RMSE 0.0066 | beats mean baseline

✓  ONNX export validated (static + dynamic batch)
   Max numerical error: 5.96e-08 (threshold 1e-5)

✓  ONNX Runtime CPU: ~5.99× faster than PyTorch
   (CPU-to-CPU measurement, Intel Core i5-1235U)

✓  QNN-ready ONNX derivative prepared
   Mod operator eliminated (336→176 nodes)
   All standard ONNX opset 17 ops — no unsupported QNN ops
   Numerical equivalence: max error = 0.0 (200 samples)
   SHA256: E2B22D8A872F1AFEF2CFD34FDE11295EC69F2BC3C4324402F284EC4F6422A62E

✓  Local inference architecture validated
   Operates independently of connectivity state

✓  Complete resilience pipeline validated
   Prediction → risk → connectivity → buffer → recovery → sync
─────────────────────────────────────────────────────────────
```

---

## Snapdragon Deployment Path

```
STEP 1 — COMPLETE
PyTorch model trained and validated
        │
        ▼
STEP 2 — COMPLETE
ONNX export with dynamic batch support
Numerical equivalence verified (max error 5.96e-8)
        │
        ▼
STEP 3 — COMPLETE (software)
QNN-ready ONNX derivative prepared
Mod operator eliminated via constant folding
336 → 176 nodes | all standard ONNX opset 17 ops
Numerical equivalence: max error = 0.0
SHA256: E2B22D8A872F1AFEF2CFD34FDE11295EC69F2BC3C4324402F284EC4F6422A62E
        │
        ▼
STEP 4 — COMPLETED
Qualcomm AI Hub QNN / HTP compilation
        │
        ▼
STEP 5 — COMPLETED
Snapdragon X Elite CRD target compilation
        │
        ▼
STEP 6 — COMPLETED — VALIDATED WORKLOAD
Qualcomm QNN / HTP execution
        │
        ▼
STEP 7 — COMPLETED — VALIDATED WORKLOAD
HTP profiling and performance evidence
  - Estimated inference time: 36 µs
  - HTP utilization: 97.22%
  - Throughput: ~3,984 inferences/sec
  - Peak inference memory: ~27.83 MiB

Full CPU ↔ Snapdragon numerical equivalence remains unverified.
```

---

## Why the Model Is Well-Suited for NPU Acceleration

The V4 model architecture has properties that align well with
Snapdragon NPU execution:

**Small parameter count:** 71,170 parameters
The model fits comfortably in NPU memory without tiling or
complex memory management.

**Fixed input shape:** [batch, 12, 17]
Deterministic input dimensions enable efficient NPU graph
compilation and static memory allocation.

**Standard operations:** Linear, LayerNorm, GELU, Softmax, Sigmoid
All operations in the V4 model are standard ONNX ops with
well-established QNN support.

**No dynamic control flow:** The forward pass is a fixed
computation graph — no conditional branches, no variable-length
sequences. This is ideal for NPU execution.

**Compact Transformer:** 2 layers, 4 heads, d_model=64
This is a deliberately small Transformer, not a large language
model. It is designed for inference efficiency.

---

## Expected Snapdragon Benefits (Unverified)

The following are **expected** benefits based on Snapdragon NPU
architecture and model characteristics. They are NOT measured values.

| Metric | Expected direction | Basis |
|---|---|---|
| Inference latency | Lower than CPU | NPU hardware acceleration |
| Power consumption | Lower than CPU | NPU power efficiency |
| Thermal behavior | Better than CPU | NPU thermal design |
| Throughput | Higher than CPU | NPU parallelism |

**None of these are claimed as verified results.**
They represent the motivation for Snapdragon deployment.

---

## Honest Status Statement

> EdgeResilience is designed for on-device deployment on
> Snapdragon-powered systems. The current validated implementation
> establishes the V4 predictive model, ONNX deployment artifact,
> local inference architecture, and reproducible software
> demonstration. Qualcomm QNN / HTP execution and Snapdragon X Elite
> component/workload validation have been demonstrated. Full
> CPU-to-Snapdragon numerical equivalence remains unverified.

This statement is strong, precise, and fully defensible.

---

## Remaining Validation Work

The Snapdragon X Elite CRD has already provided component/workload-level
execution and profiling evidence. The remaining technical work is to
resolve CPU-to-Snapdragon numerical divergence for the complete production
V4 graph before making a full end-to-end numerical-equivalence claim.

1. Preserve the Qualcomm AI Hub compile, inference, and profiling evidence already generated.
2. Complete operator-level investigation of CPU-to-Snapdragon numerical divergence.
3. Re-run the complete production-model comparison after any corrective graph/operator changes.
4. Verify numerical equivalence against the CPU reference using the established threshold of 1e-5.
5. Only after successful equivalence should a full end-to-end Snapdragon numerical-equivalence claim be made.
6. Keep physical vehicle, external CAN transmission, direct actuation, and production-vehicle validation outside the current evidence boundary.

The current status is:
`CPU_ONNX_VERIFIED_SNAPDRAGON_COMPONENT_WORKLOAD_VERIFIED`.

Full CPU-to-Snapdragon numerical equivalence remains unverified.
Operator-level investigation is in progress.
