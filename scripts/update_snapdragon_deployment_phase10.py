from pathlib import Path

p = Path("docs/SNAPDRAGON_DEPLOYMENT.md")
s = p.read_text(encoding="utf-8")

replacements = [
(
"""**Status:** CPU_AND_ONNX_VALIDATED_SNAPDRAGON_PENDING""",
"""**Status:** CPU_ONNX_VERIFIED_SNAPDRAGON_COMPONENT_WORKLOAD_VERIFIED"""
),
(
"""The deployment path to Snapdragon NPU via Qualcomm QNN is fully
prepared
but not yet hardware-verified. The current machine (Lenovo IdeaPad
3,
Intel i5-1235U) contains no Qualcomm SoC, no QNN SDK, and no
QNNExecutionProvider.""",
"""Qualcomm AI Hub has subsequently provided Snapdragon X Elite CRD
component/workload execution through Qualcomm QNN/HTP. The validated
workload was compiled for the Snapdragon X Elite target and successfully
executed and profiled on the device.

The full production-model CPU-to-Snapdragon numerical equivalence has not
yet been established. The current validation therefore distinguishes
successful Snapdragon workload execution from full-model numerical
equivalence."""
),
(
"""| QNN execution | NOT VERIFIED — requires hardware |""",
"""| QNN execution | VERIFIED — Qualcomm QNN/HTP workload |"""
),
(
"""## Qualcomm QNN — NOT VERIFIED""",
"""## Qualcomm QNN / HTP — COMPONENT / WORKLOAD VERIFIED"""
),
(
"""| QNN SDK available | NOT VERIFIED |
| QNN model conversion | NOT PERFORMED |
| QNN execution | NOT VERIFIED |
| QNN latency | NOT MEASURED |
| QNN throughput | NOT MEASURED |""",
"""| Qualcomm QNN / HTP compilation | VERIFIED — Qualcomm AI Hub |
| Snapdragon X Elite target | VERIFIED |
| QNN / HTP execution | VERIFIED — validated workload |
| HTP profiling | VERIFIED |
| Full CPU ↔ Snapdragon numerical equivalence | NOT VERIFIED |"""
),
(
"""To verify QNN execution, the following steps would be required:

1. Install Qualcomm AI Engine Direct SDK (QNN SDK)
2. Convert the ONNX model using `qnn-onnx-converter`
3. Compile the model for the target Snapdragon SoC
4. Run inference using `qnn-net-run` or the QNN Python API
5. Measure latency, throughput, and memory on the actual device
6. Record hardware version, SoC, SDK version, and execution
provider""",
"""The current evidence was generated through Qualcomm AI Hub and the
Snapdragon X Elite CRD. The remaining validation work is:

1. Investigate operator-level CPU-to-Snapdragon numerical divergence.
2. Re-run the complete production-model comparison after corrective
   graph/operator changes.
3. Verify full-model numerical equivalence against the CPU reference
   using the established 1e-5 threshold.
4. Record any revised compile, inference, and profiling evidence.
5. Keep physical vehicle, external CAN, direct actuation, and
   production-vehicle validation outside the current evidence boundary."""
),
(
"""## Snapdragon Hardware — NOT VERIFIED""",
"""## Snapdragon Hardware — COMPONENT / WORKLOAD VERIFIED"""
),
(
"""| Device | NOT VERIFIED |
| SoC | NOT VERIFIED |
| NPU execution | NOT VERIFIED |
| Accelerator utilization | NOT VERIFIED |
| Latency on Snapdragon | NOT MEASURED |
| Throughput on Snapdragon | NOT MEASURED |
| Peak memory on Snapdragon | NOT MEASURED |
| Power consumption | NOT MEASURED |
| Thermal behavior | NOT MEASURED |

No Snapdragon hardware was available during this validation phase.
All performance claims are CPU-only.""",
"""| Device | Snapdragon X Elite CRD |
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
performance."""
),
(
"""Qualcomm QNN conversion via qnn-onnx-converter (PENDING — requires
QNN SDK)
        |
        v
Snapdragon NPU execution via QNN HTP backend (PENDING — requires
hardware)
        |
        v
Edge deployment on Snapdragon-powered vehicle compute""",
"""Qualcomm AI Hub QNN / HTP compilation (VERIFIED)
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
Vehicle deployment (NOT PERFORMED)"""
),
(
"""If Snapdragon hardware and QNN SDK become available, the following
should
be measured and documented:""",
"""For further full-model validation, the following should be measured
and documented:"""
),
(
"""| QNN-ready ONNX derivative | YES (software) | Mod eliminated,
equiv PASS, awaits QNN SDK |
| Qualcomm QNN | NO | Requires QNN SDK and Snapdragon hardware |
| Snapdragon NPU | NO | Requires actual Snapdragon device |""",
"""| QNN-ready ONNX derivative | YES (software) | Mod eliminated,
source-equivalent |
| Qualcomm QNN / HTP | YES — component/workload | Snapdragon X Elite CRD |
| Snapdragon X Elite | YES — component/workload | Qualcomm SC8380XP / HTP |
| Full CPU ↔ Snapdragon equivalence | NO | Operator-level investigation ongoing |"""
),
]

for old, new in replacements:
    if old in s:
        s = s.replace(old, new, 1)
        print("[UPDATED]", old.splitlines()[0][:75])
    else:
        print("[WARN] Pattern not found:", old.splitlines()[0][:75])

p.write_text(s, encoding="utf-8")
print("SNAPDRAGON_DEPLOYMENT patch complete.")
