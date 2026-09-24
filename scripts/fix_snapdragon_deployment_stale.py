from pathlib import Path

p = Path("docs/SNAPDRAGON_DEPLOYMENT.md")
s = p.read_text(encoding="utf-8")

# 1. Replace stale QNN verification procedure
start = s.find("To verify QNN execution,")
if start >= 0:
    end_marker = "provider"
    end = s.find(end_marker, start)
    if end >= 0:
        end += len(end_marker)

        replacement = """The current evidence was generated through Qualcomm AI Hub and the
Snapdragon X Elite CRD. The remaining validation work is:

1. Investigate operator-level CPU-to-Snapdragon numerical divergence.
2. Re-run the complete production-model comparison after corrective
   graph/operator changes.
3. Verify full-model numerical equivalence against the CPU reference
   using the established 1e-5 threshold.
4. Record any revised compile, inference, and profiling evidence.
5. Keep physical vehicle, external CAN, direct actuation, and
   production-vehicle validation outside the current evidence boundary."""

        s = s[:start] + replacement + s[end:]
        print("[UPDATED] stale QNN verification procedure")
else:
    print("[WARN] stale QNN verification procedure not found")


# 2. Replace stale deployment diagram
old = """Qualcomm QNN conversion via qnn-onnx-converter (PENDING — requires
QNN SDK)
        |
        v
Snapdragon NPU execution via QNN HTP backend (PENDING — requires
hardware)
        |
        v
Edge deployment on Snapdragon-powered vehicle compute"""

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

if old in s:
    s = s.replace(old, new, 1)
    print("[UPDATED] stale deployment diagram")
else:
    print("[WARN] stale deployment diagram not found")


# 3. Replace stale comparison table
old = """| QNN-ready ONNX derivative | YES (software) | Mod eliminated, equiv
PASS, awaits QNN SDK |
| Qualcomm QNN | NO | Requires QNN SDK and Snapdragon hardware |
| Snapdragon NPU | NO | Requires actual Snapdragon device |"""

new = """| QNN-ready ONNX derivative | YES (software) | Source-equivalent |
| Qualcomm QNN / HTP | YES — component/workload | Snapdragon X Elite CRD |
| Snapdragon X Elite | YES — component/workload | Qualcomm SC8380XP / HTP |
| Full CPU ↔ Snapdragon equivalence | NO | Operator-level investigation ongoing |"""

if old in s:
    s = s.replace(old, new, 1)
    print("[UPDATED] stale deployment comparison table")
else:
    print("[WARN] stale deployment comparison table not found")


p.write_text(s, encoding="utf-8")
print("SNAPDRAGON_DEPLOYMENT stale sections fixed.")
