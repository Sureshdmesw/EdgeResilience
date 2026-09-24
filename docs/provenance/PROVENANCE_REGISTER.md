# EdgeResilience Provenance Register

| Artifact | Classification | Source | Status | Notes |
|---|---|---|---|---|
| Previous project repository | inherited/reference | GitHub repository | verified clone | Kept under inherited/ — reference only |
| Frozen CRSS Transformer checkpoint | inherited/reference | Previous project | hash verified — immutable | Not used as V4 model input |
| HCRL CAN-ID RF model | inherited/reference | Previous project commit f248869 | reference only | Not merged with V4 synthetic data |
| Phase 5.9 CAN anomaly dataset | inherited/reference | Previous project commit | reference only | Virtual laboratory data — not V4 input |
| V4 temporal dataset | new EdgeResilience artifact | This project — synthetic generation | VALIDATED | 5000 records, 17 features, 12 steps, SHA256 documented |
| V4 temporal predictor checkpoint | new EdgeResilience artifact | This project — trained from scratch | VALIDATED | MAE ~0.0051, RMSE ~0.0066 |
| V4 ONNX static export | new EdgeResilience artifact | This project | VALIDATED | Numerical equivalence verified |
| V4 ONNX dynamic export | new EdgeResilience artifact | This project | VALIDATED | Batch 1/4/16 equivalence verified, threshold 1e-5 |
| V4 inference engine | new EdgeResilience artifact | This project | VALIDATED | src/ai/v4_inference.py |
| V4 risk interpretation | new EdgeResilience artifact | This project | VALIDATED | src/resilience/v4_risk.py — deterministic demo policy |
| V4 edge runtime | new EdgeResilience artifact | This project | VALIDATED | src/resilience/v4_runtime.py |
| Connectivity policy | new EdgeResilience artifact | This project | VALIDATED | src/resilience/connectivity.py |
| Evidence buffer | new EdgeResilience artifact | This project | VALIDATED | src/resilience/evidence_buffer.py |
| Synchronization manifest | new EdgeResilience artifact | This project | VALIDATED | src/resilience/synchronization.py |
| V4 demo evidence | new EdgeResilience artifact | This project | VALIDATED | data/evidence/v4_demo_scenario.json |
| Neural ablation report | new EdgeResilience artifact | This project | VALIDATED | experiments/v4_neural_ablation_report.json |
| ONNX equivalence report | new EdgeResilience artifact | This project | VALIDATED | experiments/v4_dynamic_onnx_equivalence_report.json |
| CPU reference benchmark | new EdgeResilience artifact | This project | VALIDATED | experiments/cpu_reference_benchmark_v4.json |
| PyTorch vs ONNX CPU benchmark | new EdgeResilience artifact | This project | VALIDATED | experiments/v4_pytorch_vs_onnx_cpu_benchmark.json — CPU-to-CPU only |
| Snapdragon deployment manifest | new EdgeResilience artifact | This project | CPU_AND_ONNX_VALIDATED_SNAPDRAGON_PENDING | experiments/snapdragon_deployment_manifest_v4.json |
| Dashboard server | new EdgeResilience artifact | This project | VALIDATED | src/dashboard/server.py |
| Snapdragon hardware benchmark | new EdgeResilience artifact | This project | NOT VERIFIED | Requires actual Snapdragon environment |
| Qualcomm QNN execution | new EdgeResilience artifact | This project | NOT VERIFIED | Requires QNN runtime and Snapdragon hardware |
| Vehicle modules (CAN/HIL) | inherited/reference | Previous project | reference only | src/vehicle/*_inherited.py — not used in V4 pipeline |

## Rules

Inherited artifacts must not be presented as newly validated EdgeResilience results.

Modified inherited artifacts become separate EdgeResilience artifacts with their own provenance.

Snapdragon-specific performance claims require direct measurement or verified execution
in the relevant Snapdragon environment. CPU-to-ONNX improvement is CPU evidence only.

Virtual CAN/HIL experiments must not be represented as physical vehicle tests.

HCRL raw telemetry was NOT directly used as V4 model input. V4 uses synthetic
EdgeResilience temporal scenario data with cyber-physical features derived from
domain knowledge, not raw HCRL measurements.

The V4 dataset SHA256 is:
02a82f0f5ee78dc4e3be28b81b53b6eb4eb884600a4734f3eb3aaa279cb3a911

The V4 checkpoint SHA256 is:
b551ad9f02b56668ef3f8f7873133748275307f1934ec7fd77da14e7325d26b9
