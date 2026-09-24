from pathlib import Path

p = Path("docs/EXPERIMENT_SUMMARY.md")
s = p.read_text(encoding="utf-8")

s = s.replace(
    "| Qualcomm QNN | NOT VERIFIED |",
    "| Qualcomm QNN / HTP | VERIFIED — COMPONENT / WORKLOAD |",
    1
)

s = s.replace(
    "| Snapdragon hardware | NOT VERIFIED |",
    "| Snapdragon X Elite | VERIFIED — COMPONENT / WORKLOAD |",
    1
)

p.write_text(s, encoding="utf-8")
print("[UPDATED] EXPERIMENT_SUMMARY deployment rows")
