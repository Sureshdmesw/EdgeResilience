from pathlib import Path

ROOT = Path(r"E:\EdgeResilience\docs\submission")

replacements = {

"00_SUBMISSION_INDEX.md": [
(
"**Status:** Competition ready — V4 baseline validated",
"**Status:** Competition ready — V4 baseline + Snapdragon component/workload validation"
),
(
"""Snapdragon hardware and QNN execution are
explicitly pending hardware verification.""",
"""Snapdragon X Elite execution and Qualcomm QNN/HTP execution are
verified at the validated component/workload level. Full CPU-to-Snapdragon
numerical equivalence remains unverified and is under investigation."""
),
(
"""| Qualcomm QNN | NOT VERIFIED |
| Snapdragon hardware | NOT VERIFIED |
| NPU acceleration | NOT VERIFIED |""",
"""| Qualcomm QNN/HTP | VERIFIED — COMPONENT / WORKLOAD LEVEL |
| Snapdragon X Elite | VERIFIED — COMPONENT / WORKLOAD LEVEL |
| HTP/NPU profiling | VERIFIED — VALIDATED WORKLOAD |
| Full CPU ↔ Snapdragon numerical equivalence | NOT VERIFIED |
| Physical vehicle | NOT PERFORMED |
| External CAN | NOT PERFORMED |
| Direct actuation | NOT PERFORMED |"""
),
(
"""Snapdragon hardware and Qualcomm QNN execution
remain explicitly unverified until tested on the target platform.""",
"""Snapdragon X Elite hardware execution and Qualcomm QNN/HTP execution
have been verified for selected V4 components and the temporal-pooling +
prediction-head workload. Full CPU-to-Snapdragon numerical equivalence
remains unverified and is under investigation."""
)
],

"04_ONNX_Deployment.md": [
(
"""Qualcomm QNN conversion via qnn-onnx-converter  → PENDING
        │
        ▼
Snapdragon NPU execution                         → PENDING""",
"""Qualcomm QNN / HTP compilation and execution
        │
        ▼
Snapdragon X Elite validated workload execution
        │
        ▼
HTP profiling completed"""
),
(
"""The first two steps are complete and validated.
The final two steps require actual Snapdragon hardware and QNN SDK.""",
"""The ONNX export and CPU numerical equivalence remain validated.
Qualcomm QNN / HTP execution has subsequently been verified on a
Snapdragon X Elite CRD for selected V4 components and the temporal
pooling + prediction-head workload. Full production-model numerical
equivalence against the CPU reference remains unverified."""
),
(
"""| Qualcomm QNN | NOT VERIFIED | Requires QNN SDK + Snapdragon hardware |
| Snapdragon NPU | NOT VERIFIED | Requires actual Snapdragon device |

Overall: **CPU_AND_ONNX_VALIDATED_SNAPDRAGON_PENDING**""",
"""| Qualcomm QNN / HTP | VERIFIED — COMPONENT / WORKLOAD | Snapdragon X Elite CRD |
| Snapdragon X Elite | VERIFIED — COMPONENT / WORKLOAD | Validated V4 workload |
| HTP profiling | VERIFIED | 97.22% HTP utilization |
| Full CPU ↔ Snapdragon numerical equivalence | NOT VERIFIED | Current investigation |

Overall: **CPU_ONNX_VERIFIED_SNAPDRAGON_COMPONENT_WORKLOAD_VERIFIED**"""
)
],

"05_Snapdragon_Optimization_Path.md": [
(
"""STEP 4 — PENDING (requires QNN SDK)
Qualcomm QNN conversion""",
"""STEP 4 — COMPLETED
Qualcomm QNN / HTP compilation path executed"""
),
(
"""STEP 5 — PENDING (requires Snapdragon hardware)
Compile for target Snapdragon SoC""",
"""STEP 5 — COMPLETED
Compiled and executed on Snapdragon X Elite CRD"""
),
(
"""STEP 6 — PENDING (requires Snapdragon hardware)
Execute on Snapdragon NPU""",
"""STEP 6 — COMPLETED — VALIDATED WORKLOAD
Executed through Qualcomm QNN HTP"""
),
(
"""STEP 7 — PENDING
Measure and record:""",
"""STEP 7 — COMPLETED — VALIDATED WORKLOAD
Measured and recorded:"""
),
(
"""Until then, the status remains `CPU_AND_ONNX_VALIDATED_SNAPDRAGON_PENDING`.""",
"""The current status is:
`CPU_ONNX_VERIFIED_SNAPDRAGON_COMPONENT_WORKLOAD_VERIFIED`.

Full CPU-to-Snapdragon numerical equivalence remains unverified.
Operator-level investigation is in progress."""
),
(
"""## What Would Change This Status

If a Snapdragon-powered HP PC with Qualcomm AI Engine Direct SDK
becomes available:""",
"""## Remaining Validation Work

The Snapdragon X Elite CRD has already provided component/workload-level
execution and profiling evidence. The remaining technical work is to
resolve CPU-to-Snapdragon numerical divergence for the complete production
V4 graph before making a full end-to-end numerical-equivalence claim."""
)
],

"07_Dashboard.md": [
(
"""- CPU Reference: VERIFIED
- ONNX Runtime: VERIFIED
- Qualcomm QNN: NOT VERIFIED
- Snapdragon Hardware: NOT VERIFIED
- NPU Acceleration: NOT VERIFIED
- Overall status: CPU_AND_ONNX_VALIDATED_SNAPDRAGON_PENDING""",
"""- CPU Reference: VERIFIED
- ONNX Runtime: VERIFIED
- Snapdragon X Elite: VERIFIED — COMPONENT / WORKLOAD
- Qualcomm QNN / HTP: VERIFIED — COMPONENT / WORKLOAD
- HTP profiling: VERIFIED — VALIDATED WORKLOAD
- Full CPU ↔ Snapdragon numerical equivalence: NOT VERIFIED
- Overall status: CPU_ONNX_VERIFIED_SNAPDRAGON_COMPONENT_WORKLOAD_VERIFIED"""
)
],

"08_Reproducibility.md": [
(
"Tested on: Python 3.11.9, PyTorch 2.12.1+cpu, ONNX Runtime 1.30.0",
"Tested on: Python 3.11.9, PyTorch 2.14.0+cpu, ONNX Runtime 1.30.0"
)
],

"09_Safety_and_Provenance.md": [
(
"""| Qualcomm QNN execution | NOT VERIFIED |
| Snapdragon hardware execution | NOT VERIFIED |
| NPU acceleration | NOT VERIFIED |
| Snapdragon latency | NOT MEASURED |
| Snapdragon power | NOT MEASURED |
| Snapdragon thermal | NOT MEASURED |""",
"""| Qualcomm QNN / HTP execution | VERIFIED — COMPONENT / WORKLOAD LEVEL |
| Snapdragon X Elite execution | VERIFIED — COMPONENT / WORKLOAD LEVEL |
| HTP/NPU profiling | VERIFIED — VALIDATED WORKLOAD |
| Full CPU ↔ Snapdragon numerical equivalence | NOT VERIFIED |
| Full V4 Snapdragon latency | NOT CLAIMED |
| Snapdragon power | NOT MEASURED |
| Snapdragon thermal | NOT MEASURED |"""
),
(
"""The ~5.88× ONNX speedup is a CPU-to-CPU measurement on an Intel
Core i5-1235U. It is NOT a Snapdragon result.""",
"""The ~5.88× ONNX speedup is a CPU-to-CPU measurement on an Intel
Core i5-1235U. It is NOT a Snapdragon result.

The Snapdragon HTP profile reports approximately 36 µs estimated
inference time and 97.22% HTP utilization for the profiled workload.
These figures must not be interpreted as full V4 vehicle-system latency
or CPU-to-Snapdragon numerical equivalence."""
),
(
"""| Snapdragon hardware | PLANNED — NOT VERIFIED |
| Qualcomm QNN | PLANNED — NOT VERIFIED |""",
"""| Snapdragon X Elite | VERIFIED — COMPONENT / WORKLOAD LEVEL |
| Qualcomm QNN / HTP | VERIFIED — COMPONENT / WORKLOAD LEVEL |
| Full CPU ↔ Snapdragon numerical equivalence | NOT VERIFIED |
| Physical vehicle validation | NOT PERFORMED |"""
)
],

"10_Presentation.md": [
(
"""Snapdragon hardware and Qualcomm QNN execution
remain explicitly unverified until tested on the target platform.""",
"""Snapdragon X Elite hardware execution and Qualcomm QNN/HTP execution
have been verified at the validated component/workload level. Full
CPU-to-Snapdragon numerical equivalence remains unverified and is under
operator-level investigation."""
),
(
"""### Current deployment status

| Backend | Status |
|---|---|
| CPU reference (PyTorch) | VERIFIED |
| ONNX Runtime (CPU) | VERIFIED — ~5.88× vs PyTorch |
| Qualcomm QNN | NOT VERIFIED — pending hardware |
| Snapdragon NPU | NOT VERIFIED — pending hardware |""",
"""### Current deployment status

| Backend | Status |
|---|---|
| CPU reference (PyTorch) | VERIFIED |
| ONNX Runtime (CPU) | VERIFIED — ~5.88× vs PyTorch |
| Snapdragon X Elite | VERIFIED — COMPONENT / WORKLOAD |
| Qualcomm QNN / HTP | VERIFIED — COMPONENT / WORKLOAD |
| HTP profiling | VERIFIED — 97.22% utilization |
| Full CPU ↔ Snapdragon numerical equivalence | NOT VERIFIED |
| Physical vehicle | NOT PERFORMED |"""
),
(
"""This is not a vague "could run on Snapdragon" claim.
It is a specific, documented, step-by-step path using Qualcomm's
own toolchain, waiting only for access to the target hardware.""",
"""This is not a hypothetical Snapdragon path. Component and workload-level
execution has been demonstrated on a Snapdragon X Elite CRD through
Qualcomm QNN/HTP. The remaining limitation is full production-model
CPU-to-Snapdragon numerical equivalence."""
),
(
"""- Already 5.88× faster with ONNX Runtime on CPU — NPU will go further""",
"""- HTP profiling has measured 97.22% HTP utilization for the validated
  temporal-pooling + prediction-head workload
- The profiled workload reports an estimated 36 µs inference time
- These measurements are workload-specific and are not claimed as
  full V4 system latency or acceleration vs CPU"""
),
(
"""## Future Roadmap

1. **Snapdragon hardware verification** — QNN conversion, NPU execution,
   latency/power/thermal measurement on actual Snapdragon device""",
"""## Remaining Roadmap

1. **Complete Snapdragon numerical validation** — resolve operator-level
   CPU-to-Snapdragon divergence and establish full production-model
   numerical equivalence before making an end-to-end equivalence claim.

2. **Extended Snapdragon benchmarking** — measure complete production-graph
   latency, throughput, memory, power and thermal behavior under a clearly
   defined benchmark protocol."""
)
]
}

for name, pairs in replacements.items():
    path = ROOT / name
    text = path.read_text(encoding="utf-8")
    original = text

    for old, new in pairs:
        if old not in text:
            print(f"[WARN] Pattern not found in {name}: {old[:100]!r}")
        else:
            text = text.replace(old, new, 1)

    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"[UPDATED] {name}")
    else:
        print(f"[UNCHANGED] {name}")
