from pathlib import Path

# ------------------------------------------------------------
# EVIDENCE_INDEX.md
# ------------------------------------------------------------
p = Path("docs/EVIDENCE_INDEX.md")
s = p.read_text(encoding="utf-8")

s = s.replace(
    "CPU_AND_ONNX_VALIDATED_SNAPDRAGON_PENDING",
    "CPU_ONNX_VERIFIED_SNAPDRAGON_COMPONENT_WORKLOAD_VERIFIED"
)

s = s.replace(
    "No Snapdragon hardware measurements are included",
    "Snapdragon X Elite workload measurements are included; full CPU-to-Snapdragon numerical equivalence remains unverified"
)

p.write_text(s, encoding="utf-8")
print("[UPDATED] EVIDENCE_INDEX.md")


# ------------------------------------------------------------
# EXPERIMENT_SUMMARY.md
# ------------------------------------------------------------
p = Path("docs/EXPERIMENT_SUMMARY.md")
s = p.read_text(encoding="utf-8")

s = s.replace(
    "Overall status: CPU_AND_ONNX_VALIDATED_SNAPDRAGON_PENDING",
    "Overall status: CPU_ONNX_VERIFIED_SNAPDRAGON_COMPONENT_WORKLOAD_VERIFIED"
)

s = s.replace(
    "No Snapdragon hardware was available",
    "Snapdragon X Elite CRD workload execution and HTP profiling were subsequently validated"
)

p.write_text(s, encoding="utf-8")
print("[UPDATED] EXPERIMENT_SUMMARY.md")


# ------------------------------------------------------------
# REPRODUCIBILITY.md
# ------------------------------------------------------------
p = Path("docs/REPRODUCIBILITY.md")
s = p.read_text(encoding="utf-8")

s = s.replace(
    "No Snapdragon hardware was available during this validation.",
    "Snapdragon X Elite CRD component/workload execution and HTP profiling were subsequently validated through Qualcomm AI Hub."
)

p.write_text(s, encoding="utf-8")
print("[UPDATED] REPRODUCIBILITY.md")

print("Repository documentation status patch complete.")
