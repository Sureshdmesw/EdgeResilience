from pathlib import Path

p = Path("README.md")
s = p.read_text(encoding="utf-8")

replacements = [
(
"""**Status:** Competition ready — V4 baseline validated""",
"""**Status:** Competition ready — V4 baseline + Snapdragon component/workload validation"""
),
(
"""The model is exported to ONNX for deployment. The deployment path to
Snapdragon NPU via Qualcomm QNN is architecturally prepared and pending
hardware verification.""",
"""The model is exported to ONNX for deployment. Qualcomm AI Hub has been
used to compile and execute a validated V4 workload on a Snapdragon X Elite
CRD through Qualcomm QNN/HTP. HTP profiling has also been completed.
Full CPU-to-Snapdragon numerical equivalence remains under investigation."""
),
(
"""- Deployment status (ONNX verified, Snapdragon NOT VERIFIED)""",
"""- Deployment status (ONNX verified, Snapdragon component/workload validated)"""
),
(
"""| Qualcomm QNN | NOT VERIFIED |
| Snapdragon hardware | NOT VERIFIED |
| NPU acceleration | NOT VERIFIED |""",
"""| Qualcomm QNN / HTP | VERIFIED — COMPONENT / WORKLOAD |
| Snapdragon X Elite | VERIFIED — COMPONENT / WORKLOAD |
| HTP profiling | VERIFIED — VALIDATED WORKLOAD |
| Full CPU ↔ Snapdragon numerical equivalence | NOT VERIFIED |"""
),
(
"""The ONNX model is ready for Qualcomm QNN conversion. Hardware verification
requires an actual Snapdragon device and QNN SDK.

The ~5.99x ONNX speedup is a CPU-to-CPU measurement on an Intel Core i5-1235U.
It is NOT a Snapdragon result.""",
"""Qualcomm QNN / HTP execution has been validated on a Snapdragon X Elite
CRD for the tested V4 workload. The profiled workload achieved an estimated
36 µs inference time and 97.22% HTP utilization.

These are workload-specific measurements and are not full vehicle-system
latency measurements. The ~5.99x ONNX speedup is a CPU-to-CPU measurement
on an Intel Core i5-1235U and is NOT a Snapdragon result.

Full CPU-to-Snapdragon numerical equivalence remains NOT VERIFIED."""
),
(
"""3. Snapdragon hardware execution not yet verified""",
"""3. Full CPU-to-Snapdragon numerical equivalence remains under investigation"""
),
(
"""1. Snapdragon hardware deployment and QNN conversion""",
"""1. Resolve CPU-to-Snapdragon numerical divergence and complete full-model validation"""
),
]

for old, new in replacements:
    if old in s:
        s = s.replace(old, new, 1)
        print("[UPDATED]", old.splitlines()[0][:70])
    else:
        print("[WARN] Pattern not found:", old.splitlines()[0][:70])

p.write_text(s, encoding="utf-8")
print("README patch complete.")
