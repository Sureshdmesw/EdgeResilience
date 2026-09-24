# EdgeResilience — Experiment Summary

All numbers in this document come directly from existing evidence artifacts.
No results have been recomputed or altered.

---

## 1. V4 Dataset Validation

| Property | Value | Source |
|---|---|---|
| Records | 5,000 | edgeresilience_temporal_dataset_v4_manifest.json |
| Features per step | 17 | dataset manifest |
| Observation steps | 12 | dataset manifest |
| SHA256 | 02a82f0f5ee78dc4e3be28b81b53b6eb4eb884600a4734f3eb3aaa279cb3a911 | verified |
| Generation | Synthetic EdgeResilience temporal scenarios | dataset manifest |
| Latent regimes | Used during generation — NOT exposed as features | dataset manifest |

---

## 2. V4 Target Predictability

The mean-prediction baseline was computed to confirm the target is
non-trivial and the model provides genuine predictive value.

| Metric | V4 Model | Mean Baseline |
|---|---|---|
| MAE | 0.0051 | 0.0203 |
| RMSE | 0.0066 | 0.0232 |
| Beats baseline | YES | — |

Source: models/edgeresilience/temporal_predictor_v4_report.json

---

## 3. Temporal Information Benchmark (Neural Ablation)

Three input representations compared on the V4 dataset:

| Input representation | MAE | RMSE | Notes |
|---|---|---|---|
| Final timestep only | 0.0067 | 0.0086 | Weakest |
| Final + delta + std (compact) | 0.0053 | 0.0068 | Close to full |
| Full 12-step sequence (V4) | 0.0052 | 0.0066 | Best — production config |

Conclusion: temporal trajectory information improves prediction.
The full-sequence Transformer is the strongest tested configuration.

Source: experiments/v4_neural_ablation_report.json

---

## 4. V4 Training

| Parameter | Value |
|---|---|
| Optimizer | AdamW |
| Learning rate | 0.001 |
| Weight decay | 0.0001 |
| Batch size | 128 |
| Max epochs | 80 |
| Best epoch | 77 |
| Best validation loss | 4.378e-05 |
| Random seed | 42 |
| Train / val / test | 3200 / 800 / 1000 |
| Device | CPU |

Source: models/edgeresilience/temporal_predictor_v4_report.json

---

## 5. V4 Inference Validation

The V4InferenceEngine loads the checkpoint, validates the 17-feature
contract, applies stored normalization, and runs the Transformer forward pass.

Validated behavior:
- Correct feature count enforcement (17)
- Correct sequence length enforcement (12)
- Normalization applied from checkpoint
- Output is scalar in [0, 1]

Source: src/ai/v4_inference.py

---

## 6. ONNX Static Export

| Property | Value |
|---|---|
| Artifact | temporal_predictor_v4.onnx |
| Input shape | [1, 12, 17] |
| Output shape | [1] |
| ONNX opset | 17 |
| Export status | PASS |
| Max absolute error vs PyTorch | 7.45e-08 |
| Mean absolute error | 2.39e-08 |
| Provider | CPUExecutionProvider |

Source: experiments/v4_onnx_export_report.json, experiments/v4_onnx_equivalence_report.json

---

## 7. ONNX Dynamic Export

| Property | Value |
|---|---|
| Artifact | temporal_predictor_v4_dynamic.onnx |
| Input shape | [batch, 12, 17] |
| Output shape | [batch] |
| Export status | PASS |

Source: experiments/v4_dynamic_onnx_export_report.json

---

## 8. Dynamic ONNX Equivalence

| Batch size | Max absolute error | Threshold | Result |
|---|---|---|---|
| 1 | 4.38e-08 | 1e-05 | PASS |
| 4 | 3.54e-08 | 1e-05 | PASS |
| 16 | 5.96e-08 | 1e-05 | PASS |

Source: experiments/v4_dynamic_onnx_equivalence_report.json

---

## 9. V4 Runtime Scenario Validation

Three-cycle software demonstration:

| Cycle | Connectivity | Degradation | Risk | Buffering | Recovery | Sync |
|---|---|---|---|---|---|---|
| cycle-001 | CONNECTED | 0.033857 | LOW | No | No | No |
| cycle-002 | DISCONNECTED | 0.003141 | NORMAL | Yes | No | No |
| cycle-003 | CONNECTED | 0.043561 | MEDIUM | No | Yes | Yes |

Assertions verified:
- cycle-003 recovery_detected = True
- cycle-003 synchronization_ready = True
- cycle-003 local_buffering_required = False

Source: data/evidence/v4_demo_scenario.json

---

## 10. CPU Reference Benchmark

| Metric | Value |
|---|---|
| Hardware | Intel Core i5-1235U |
| Input shape | [1000, 12, 17] |
| Samples per run | 1,000 |
| Warmup runs | 20 |
| Benchmark runs | 100 |
| Mean batch latency | 29.59 ms |
| Median batch latency | 29.29 ms |
| P95 batch latency | 34.92 ms |
| Throughput | 33,800 samples/sec |

This is a CPU reference measurement. No Snapdragon performance is claimed.

Source: experiments/cpu_reference_benchmark_v4.json

---

## 11. PyTorch vs ONNX CPU Benchmark

| Backend | Mean latency | Median latency | P95 latency |
|---|---|---|---|
| PyTorch (CPU) | 1.570 ms | 1.254 ms | 4.558 ms |
| ONNX Runtime (CPU) | 0.267 ms | 0.252 ms | 0.331 ms |
| Speedup (mean) | ~5.88x | — | — |

Hardware: Intel Core i5-1235U. CPU-to-CPU measurement only.
NOT a Snapdragon result. NOT an NPU result.

Source: experiments/v4_pytorch_vs_onnx_cpu_benchmark.json

---

## 12. Deployment Audit

| Backend | Status |
|---|---|
| CPU reference | VERIFIED |
| ONNX Runtime (CPU) | VERIFIED |
| Qualcomm QNN / HTP | VERIFIED — COMPONENT / WORKLOAD |
| Snapdragon X Elite | VERIFIED — COMPONENT / WORKLOAD |

Overall status: CPU_ONNX_VERIFIED_SNAPDRAGON_COMPONENT_WORKLOAD_VERIFIED

Source: experiments/snapdragon_deployment_manifest_v4.json

---

## Notes

- All experiments use synthetic V4 data — not raw vehicle telemetry
- All benchmarks performed on Windows / Intel Core i5-1235U
- Snapdragon X Elite CRD workload execution and HTP profiling were subsequently validated
- The PyTorch UserWarning about nested tensors is benign (norm_first=True)
