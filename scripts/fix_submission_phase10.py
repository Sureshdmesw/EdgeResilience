from pathlib import Path

root = Path(r"E:\EdgeResilience\docs\submission")

# 00: remove duplicated safety rows
p = root / "00_SUBMISSION_INDEX.md"
s = p.read_text(encoding="utf-8")

duplicate = """| Physical vehicle | NOT PERFORMED |
| External CAN | NOT PERFORMED |
| Direct actuation | NOT PERFORMED |
"""

# Keep only the first occurrence of this exact 3-row block.
first = s.find(duplicate)
if first >= 0:
    second = s.find(duplicate, first + len(duplicate))
    if second >= 0:
        s = s[:second] + s[second + len(duplicate):]

p.write_text(s, encoding="utf-8")

# 04: replace stale deployment diagram
p = root / "04_ONNX_Deployment.md"
s = p.read_text(encoding="utf-8")

old = """Qualcomm QNN conversion via qnn-onnx-converter  ← PENDING
        │
        ▼
Snapdragon NPU execution                         ← PENDING"""

new = """Qualcomm QNN / HTP compilation
        │
        ▼
Snapdragon X Elite validated workload execution
        │
        ▼
HTP profiling completed"""

if old in s:
    s = s.replace(old, new, 1)

p.write_text(s, encoding="utf-8")

# 06: update safety/deployment boundary
p = root / "06_Working_Demo.md"
s = p.read_text(encoding="utf-8")

old = """Snapdragon hardware:         NOT VERIFIED
Qualcomm QNN:                NOT VERIFIED"""

new = """Snapdragon X Elite:          VERIFIED — COMPONENT / WORKLOAD
Qualcomm QNN / HTP:          VERIFIED — COMPONENT / WORKLOAD
Full CPU ↔ Snapdragon numerical equivalence: NOT VERIFIED"""

if old in s:
    s = s.replace(old, new, 1)

p.write_text(s, encoding="utf-8")

print("Submission cleanup complete.")
