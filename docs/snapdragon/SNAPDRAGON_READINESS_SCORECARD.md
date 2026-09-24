# EdgeResilience — Snapdragon Readiness Scorecard

**Phase:** PHASE_17_SNAPDRAGON_READINESS_SCORECARD
**Generated:** See experiments/snapdragon/snapdragon_deployment_manifest.json

This is a factual checklist. No subjective scores.

---

## Scorecard

| Capability | Status | Evidence |
|---|---|---|
| CPU reference (PyTorch) | VERIFIED | experiments/cpu_reference_benchmark_v4.json |
| ONNX export | VERIFIED | experiments/v4_onnx_export_report.json |
| ONNX dynamic batch | VERIFIED | experiments/v4_dynamic_onnx_export_report.json |
| ONNX numerical equivalence | VERIFIED | experiments/v4_dynamic_onnx_equivalence_report.json |
| ONNX CPU speedup | VERIFIED | experiments/v4_pytorch_vs_onnx_cpu_benchmark.json |
| QNN-ready derivative prepared | VERIFIED | experiments/snapdragon/qnn_ready_model_report.json |
| QNN-ready derivative equivalence | VERIFIED | experiments/snapdragon/qnn_ready_model_report.json |
| QNN-ready ONNX checker | VERIFIED | experiments/snapdragon/model_compatibility_report.json |
| QNN operator compatibility (theoretical) | VERIFIED | experiments/snapdragon/model_compatibility_report.json |
| Snapdragon hardware | NOT VERIFIED | No Qualcomm SoC present on current machine |
| Qualcomm QNN SDK | NOT VERIFIED | Not installed |
| QNN conversion (qnn-onnx-converter) | NOT VERIFIED | Requires QNN SDK |
| QNN CPU backend execution | NOT VERIFIED | Requires Snapdragon hardware |
| QNN GPU backend execution | NOT VERIFIED | Requires Snapdragon hardware |
| QNN HTP/NPU backend execution | NOT VERIFIED | Requires Snapdragon hardware |
| Snapdragon execution | NOT VERIFIED | Requires Snapdragon hardware |
| NPU execution | NOT VERIFIED | Requires Snapdragon hardware |
| Snapdragon numerical equivalence | NOT VERIFIED | Requires hardware execution |
| Snapdragon latency | NOT VERIFIED | Requires hardware execution |
| Snapdragon throughput | NOT VERIFIED | Requires hardware execution |
| Snapdragon memory | NOT VERIFIED | Requires hardware execution |
| Snapdragon power | NOT VERIFIED | Requires hardware execution |
| Snapdragon thermal | NOT VERIFIED | Requires hardware execution |
| Reproducibility (software steps) | VERIFIED | docs/snapdragon/REPRODUCE_SNAPDRAGON.md |
| Reproducibility (hardware steps) | PLANNED | docs/snapdragon/REPRODUCE_SNAPDRAGON.md |
| Protected artifact integrity | VERIFIED | _integrity_check.py — all PASS |

---

## Summary

| Category | VERIFIED | NOT VERIFIED | PLANNED |
|---|---|---|---|
| Software baseline | 9 | 0 | 0 |
| Snapdragon hardware | 0 | 15 | 1 |

**Overall deployment status:** CPU_AND_ONNX_VALIDATED_SNAPDRAGON_PENDING
