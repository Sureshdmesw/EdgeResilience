from pathlib import Path

p = Path(r"docs/submission/05_Snapdragon_Optimization_Path.md")
s = p.read_text(encoding="utf-8")

old = """1. Install QNN SDK
2. Run `qnn-onnx-converter` on `temporal_predictor_v4_qnn_ready.onnx` (QNN-ready derivative already prepared)
3. Compile for target Snapdragon SoC
4. Execute on Snapdragon NPU
5. Capture latency, throughput, memory, and power
6. Compare Snapdragon output against CPU reference
7. Create new evidence artifact: `experiments/snapdragon/snapdragon_v4_benchmark.json`
8. Update deployment manifest status to `SNAPDRAGON_VERIFIED`"""

new = """1. Preserve the Qualcomm AI Hub compile and profile evidence already generated.
2. Preserve the Snapdragon X Elite CRD execution artifacts and job identifiers.
3. Complete operator-level investigation of CPU-to-Snapdragon numerical divergence.
4. Re-run full production-model comparison after any corrective graph/operator changes.
5. Only then consider a full end-to-end CPU-to-Snapdragon numerical-equivalence claim.
6. Continue to keep physical vehicle, external CAN, direct actuation, and production-vehicle validation outside the current evidence boundary."""

if old not in s:
    print("[WARN] Remaining-work block not found")
else:
    s = s.replace(old, new, 1)
    print("[UPDATED] 05_Snapdragon_Optimization_Path.md")

p.write_text(s, encoding="utf-8")
