from pathlib import Path

p = Path("docs/SNAPDRAGON_DEPLOYMENT.md")
s = p.read_text(encoding="utf-8")

# Remove the old pending deployment diagram by locating its first distinctive line
start = s.find("Qualcomm QNN conversion via qnn-onnx-converter")
if start >= 0:
    end = s.find("Edge deployment on Snapdragon-powered vehicle compute", start)
    if end >= 0:
        end += len("Edge deployment on Snapdragon-powered vehicle compute")

        new = """Qualcomm AI Hub QNN / HTP compilation (VERIFIED)
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

        s = s[:start] + new + s[end:]
        print("[UPDATED] SNAPDRAGON_DEPLOYMENT deployment diagram")
    else:
        print("[WARN] deployment diagram end marker not found")
else:
    print("[WARN] old deployment diagram not found")


# Replace stale comparison-table rows individually
s = s.replace(
    "| QNN-ready ONNX derivative | YES (software) | Mod eliminated, equiv\nPASS, awaits QNN SDK |",
    "| QNN-ready ONNX derivative | YES (software) | Source-equivalent |",
    1
)

s = s.replace(
    "| Qualcomm QNN | NO | Requires QNN SDK and Snapdragon hardware |",
    "| Qualcomm QNN / HTP | YES — component/workload | Snapdragon X Elite CRD |",
    1
)

s = s.replace(
    "| Snapdragon NPU | NO | Requires actual Snapdragon device |",
    "| Snapdragon X Elite | YES — component/workload | Qualcomm SC8380XP / HTP |",
    1
)

# Add the explicit full-model limitation immediately after the Snapdragon row
needle = "| Snapdragon X Elite | YES — component/workload | Qualcomm SC8380XP / HTP |"
if needle in s and "| Full CPU ↔ Snapdragon equivalence | NO | Operator-level investigation ongoing |" not in s:
    s = s.replace(
        needle,
        needle + "\n| Full CPU ↔ Snapdragon equivalence | NO | Operator-level investigation ongoing |",
        1
    )

p.write_text(s, encoding="utf-8")
print("SNAPDRAGON_DEPLOYMENT remaining stale sections fixed.")
