from pathlib import Path

# ------------------------------------------------------------
# 05 — Snapdragon Optimization Path
# ------------------------------------------------------------
p = Path(r"docs/submission/05_Snapdragon_Optimization_Path.md")
s = p.read_text(encoding="utf-8")

old_diagram = """STEP 4 — COMPLETED
Qualcomm QNN / HTP compilation path executed
  qnn-onnx-converter \\
    --input_network temporal_predictor_v4_qnn_ready.onnx \\
    --input_dim vehicle_temporal_features 1,12,17
        │
        ▼
STEP 5 — COMPLETED
Compiled and executed on Snapdragon X Elite CRD
  qnn-model-lib-generator
        │
        ▼
STEP 6 — COMPLETED — VALIDATED WORKLOAD
Executed through Qualcomm QNN HTP
  qnn-net-run --backend HtpBackend
        │
        ▼
STEP 7 — COMPLETED — VALIDATED WORKLOAD
Measured and recorded:
  - Latency (mean, median, P95)
  - Throughput (inferences/sec)
  - Memory footprint
  - Power consumption (if measurement API available)
  - Numerical equivalence vs CPU reference"""

new_diagram = """STEP 4 — COMPLETED
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

Full CPU ↔ Snapdragon numerical equivalence remains unverified."""

if old_diagram in s:
    s = s.replace(old_diagram, new_diagram, 1)
    print("[UPDATED] 05 execution path")
else:
    print("[WARN] 05 execution diagram not found")

old_status = """> EdgeResilience is designed for on-device deployment on
> Snapdragon-powered HP PCs. The current validated implementation
> establishes the V4 predictive model, ONNX deployment artifact,
> local inference architecture, and reproducible software
> demonstration. Snapdragon hardware and Qualcomm QNN execution
> remain explicitly unverified until tested on the target platform."""

new_status = """> EdgeResilience is designed for on-device deployment on
> Snapdragon-powered systems. The current validated implementation
> establishes the V4 predictive model, ONNX deployment artifact,
> local inference architecture, and reproducible software
> demonstration. Qualcomm QNN / HTP execution and Snapdragon X Elite
> component/workload validation have been demonstrated. Full
> CPU-to-Snapdragon numerical equivalence remains unverified."""

if old_status in s:
    s = s.replace(old_status, new_status, 1)
    print("[UPDATED] 05 status statement")
else:
    print("[WARN] 05 status statement not found")

old_remaining = """1. Install QNN SDK
2. Run `qnn-onnx-converter` on `temporal_predictor_v4_qnn_ready.onnx` (QNN-ready derivative already prepared)
3. Compile for target SoC
4. Execute with `qnn-net-run --backend HtpBackend`
5. Verify numerical equivalence vs CPU reference (threshold 1e-5)
6. Record latency, throughput, memory
7. Create new evidence artifact: `experiments/snapdragon/snapdragon_v4_benchmark.json`
8. Update deployment manifest status to `SNAPDRAGON_VERIFIED`"""

new_remaining = """1. Preserve the Qualcomm AI Hub compile, inference, and profiling evidence already generated.
2. Complete operator-level investigation of CPU-to-Snapdragon numerical divergence.
3. Re-run the complete production-model comparison after any corrective graph/operator changes.
4. Verify numerical equivalence against the CPU reference using the established threshold of 1e-5.
5. Only after successful equivalence should a full end-to-end Snapdragon numerical-equivalence claim be made.
6. Keep physical vehicle, external CAN transmission, direct actuation, and production-vehicle validation outside the current evidence boundary."""

if old_remaining in s:
    s = s.replace(old_remaining, new_remaining, 1)
    print("[UPDATED] 05 remaining validation work")
else:
    print("[WARN] 05 remaining-work block not found")

p.write_text(s, encoding="utf-8")


# ------------------------------------------------------------
# 10 — Presentation
# ------------------------------------------------------------
p = Path(r"docs/submission/10_Presentation.md")
s = p.read_text(encoding="utf-8")

old = """ONNX model (validated, dynamic batch)
        │
        ▼
qnn-onnx-converter → QNN model
        │
        ▼
qnn-model-lib-generator → compiled for target SoC
        │
        ▼
qnn-net-run --backend HtpBackend → NPU execution"""

new = """ONNX model (validated, dynamic batch)
        │
        ▼
Qualcomm AI Hub QNN / HTP compilation
        │
        ▼
Snapdragon X Elite CRD target execution
        │
        ▼
HTP profiling and performance evidence"""

if old in s:
    s = s.replace(old, new, 1)
    print("[UPDATED] 10 deployment path")
else:
    print("[WARN] 10 deployment diagram not found")

p.write_text(s, encoding="utf-8")

print("Phase 10 submission documentation patch complete.")
