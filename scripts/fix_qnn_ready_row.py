from pathlib import Path

p = Path("docs/SNAPDRAGON_DEPLOYMENT.md")
s = p.read_text(encoding="utf-8")

old = """| QNN-ready ONNX derivative | YES (software) | Mod eliminated, equiv
PASS, awaits QNN SDK |"""

new = """| QNN-ready ONNX derivative | YES (software) | Source-equivalent |"""

if old in s:
    s = s.replace(old, new, 1)
    print("[UPDATED] QNN-ready ONNX derivative row")
else:
    print("[WARN] QNN-ready row not found")

p.write_text(s, encoding="utf-8")
