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
| Snapdragon hardware | VERIFIED | Snapdragon X Elite CRD validation target |
| Qualcomm QNN SDK | VERIFIED FOR AI Hub/HTP WORKFLOW | QAI Hub production profile evidence |
| QNN conversion (qnn-onnx-converter) | VERIFIED FOR DEPLOYMENT WORKFLOW | QNN-ready production artifact/profile evidence |
| QNN CPU backend execution | NOT ASSESSED | Not part of the validated HTP path |
| QNN GPU backend execution | NOT ASSESSED | Not part of the validated HTP path |
| QNN HTP/NPU backend execution | VERIFIED | Snapdragon X Elite CRD production HTP profile |
| Snapdragon execution | VERIFIED | Snapdragon X Elite CRD production profile |
| NPU execution | VERIFIED | 90/90 production profile entries |
| Snapdragon numerical equivalence | FAILED | Max abs error 0.0030923495; full-model equivalence threshold not met |
| Snapdragon latency | VERIFIED | 63 us estimated; 67 us warm median; 68.96 us warm mean |
| Snapdragon throughput | VERIFIED WITH LIMITATION | ~14,501/s warm single-batch profile estimate |
| Snapdragon memory | VERIFIED | 28.5 MB peak profile memory |
| Snapdragon power | NOT VERIFIED | No power telemetry |
| Snapdragon thermal | NOT VERIFIED | No thermal telemetry |
| Reproducibility (software steps) | VERIFIED | docs/snapdragon/REPRODUCE_SNAPDRAGON.md |
| Reproducibility (hardware steps) | PLANNED | docs/snapdragon/REPRODUCE_SNAPDRAGON.md |
| Protected artifact integrity | VERIFIED | _integrity_check.py — all PASS |

---

## Summary

| Category | VERIFIED | NOT VERIFIED | PLANNED |
|---|---|---|---|
| Software baseline | 9 | 0 | 0 |
| Snapdragon hardware | 0 | 15 | 1 |

**Overall deployment status:** SNAPDRAGON_FULL_PRODUCTION_HTP_PROFILE_VERIFIED_NUMERICAL_EQUIVALENCE_FAIL_POWER_THERMAL_UNVERIFIED
