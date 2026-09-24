# EdgeResilience — Final Technical Baseline

**Project:** EdgeResilience: Snapdragon-Powered Predictive Intelligence for Connected Vehicle Safety
**Competition:** Qualcomm Snapdragon AI Lab Build and Present Challenge
**Status:** COMPETITION READY

---

## 1. Project Purpose

EdgeResilience demonstrates a complete edge AI pipeline for connected vehicle
cyber-physical safety. The system predicts future resilience degradation from
temporal cyber telemetry observations, maintains local inference when
connectivity is lost, buffers evidence locally, detects connectivity recovery,
and prepares a synchronization manifest when the connection is restored.

The project is designed for deployment on Snapdragon-powered edge compute.
CPU and ONNX deployment are validated. Snapdragon hardware execution is
explicitly pending actual hardware verification.

---

## 2. Real-World Problem

Connected vehicles are exposed to cyber threats including CAN bus anomalies,
message injection, timing manipulation, and payload tampering. When a vehicle
loses connectivity to a cloud or infrastructure backend, it must continue to
operate safely using only local compute. Evidence of anomalous behavior must
be preserved locally and synchronized when connectivity recovers.

The problem has three dimensions:

1. Predictive: detect degradation before it becomes critical
2. Resilient: maintain local intelligence when connectivity is lost
3. Auditable: preserve tamper-evident evidence for post-event analysis

---

## 3. Problem Statement

Given a temporal sequence of cyber telemetry observations from a connected
vehicle, predict the future resilience degradation of the system, maintain
local inference and evidence buffering during connectivity loss, and
synchronize buffered evidence when connectivity recovers.

---

## 4. System Architecture

```
Vehicle / Cyber Observations (17 features x 12 steps)
        |
        v
[V4 Temporal Predictor — EdgeResilienceTemporalPredictor]
        |
        v
Predicted Future Degradation (scalar, 0-1)
        |
        v
[Deterministic Risk Interpretation — V4_DEGRADATION_DEMO_POLICY_V1]
        |
        v
Risk Level: NORMAL / LOW / MEDIUM / HIGH / CRITICAL
        |
        v
[Connectivity State Evaluation]
        |
        v
CONNECTED / DEGRADED / DISCONNECTED
        |
        +---> Local Inference (always allowed)
        |
        +---> Evidence Buffer (when risk >= MEDIUM or connectivity degraded)
        |
        +---> Recovery Detection (DISCONNECTED -> CONNECTED transition)
        |
        v
Synchronization Manifest (software manifest — no network transmission)
        |
        v
Auditable Evidence Record (SHA-256 hashed, timestamped)
```

Deployment layer:

```
PyTorch checkpoint (CPU reference)
        |
        v
ONNX Runtime (CPU — VERIFIED)
        |
        v
[PLANNED] Qualcomm QNN / Snapdragon NPU (NOT VERIFIED)
```

---

## 5. V4 Model Architecture — VALIDATED

**Classification:** new EdgeResilience artifact

| Parameter | Value |
|---|---|
| Model name | EdgeResilience_V4_TemporalPredictor |
| Architecture | Temporal Transformer |
| Input features | 17 |
| Sequence length | 12 observation steps |
| d_model | 64 |
| Attention heads | 4 |
| Transformer layers | 2 |
| Feed-forward dimension | 128 |
| Dropout | 0.1 |
| Pooling | Temporal attention pooling |
| Output | Predicted future degradation (scalar, Sigmoid) |
| Parameters | 71,170 |
| Checkpoint | models/edgeresilience/temporal_predictor_v4.pt |

The model uses a learned temporal attention pooling mechanism that weights
each of the 12 observation steps by their relevance to the prediction target.
This is distinct from simple mean pooling or final-step extraction.

---

## 6. 17-Feature Input Contract — VALIDATED

The V4 model operates on 17 EdgeResilience cyber/resilience features per
observation step. These are synthetic scenario features derived from
cyber-physical domain knowledge. They are NOT raw HCRL measurements.

| # | Feature |
|---|---|
| 1 | cyber_message_rate |
| 2 | cyber_unique_can_id_count |
| 3 | cyber_can_id_entropy |
| 4 | cyber_mean_interarrival_ms |
| 5 | cyber_std_interarrival_ms |
| 6 | cyber_min_interarrival_ms |
| 7 | cyber_max_interarrival_ms |
| 8 | cyber_interarrival_cv |
| 9 | cyber_payload_change_rate |
| 10 | cyber_mean_hamming_distance |
| 11 | cyber_dlc_change_rate |
| 12 | cyber_dominant_can_id_fraction |
| 13 | cyber_burst_score |
| 14 | cyber_timing_anomaly_score |
| 15 | cyber_payload_anomaly_score |
| 16 | cyber_id_anomaly_score |
| 17 | cyber_attack_score |

---

## 7. 12-Step Temporal Input — VALIDATED

Each inference call receives 12 consecutive observation steps. The temporal
window captures the trajectory of cyber telemetry over time, enabling the
model to detect trends, bursts, and gradual degradation patterns that are
invisible to single-step models.

The temporal ablation experiment confirmed that the full 12-step sequence
outperforms both final-step-only and compact summary representations.

---

## 8. V4 Dataset Provenance — VALIDATED

**Classification:** new EdgeResilience synthetic artifact

| Property | Value |
|---|---|
| Path | data/processed/temporal/edgeresilience_temporal_dataset_v4.jsonl |
| Records | 5,000 |
| Features per step | 17 |
| Observation steps | 12 |
| Generation method | Synthetic EdgeResilience temporal scenario generation |
| Latent regimes | Used during generation — NOT exposed as model features |
| Hidden temporal memory | Used during generation — NOT exposed as model features |
| Target | future_degradation (continuous, 0-1) |
| SHA256 | 02a82f0f5ee78dc4e3be28b81b53b6eb4eb884600a4734f3eb3aaa279cb3a911 |

**Important distinctions:**

- Raw HCRL records are NOT the direct model input
- Cyber values are synthetic scenario features, not raw HCRL measurements
- The latent regime used during generation is not exposed to the model
- This dataset must not be described as raw vehicle telemetry

---

## 9. Training Configuration — VALIDATED

| Parameter | Value |
|---|---|
| Optimizer | AdamW |
| Learning rate | 0.001 |
| Weight decay | 0.0001 |
| Batch size | 128 |
| Max epochs | 80 |
| Best epoch | 77 |
| Random seed | 42 |
| Train samples | 3,200 |
| Validation samples | 800 |
| Test samples | 1,000 |
| Split | 80/20 train-test, then 80/20 train-validation |
| Device | CPU |

---

## 10. Validation Methodology — VALIDATED

The dataset was split 80/20 into train and test pools using seed 42.
The training pool was further split 80/20 into train and validation sets.
The test set was held out and used only for final evaluation.

The model was selected at the epoch with the lowest validation loss.
Final metrics were computed on the held-out test set.

A mean-prediction baseline was computed to confirm the model provides
genuine predictive value beyond a trivial baseline.

---

## 11. V4 Test Metrics — VALIDATED

| Metric | V4 Model | Mean Baseline |
|---|---|---|
| MAE | 0.0051 | 0.0203 |
| RMSE | 0.0066 | 0.0232 |
| Beats baseline | YES | — |

Best validation loss: 4.378e-05

---

## 12. Temporal Ablation — VALIDATED

Three input representations were compared on the same V4 dataset:

| Input representation | MAE | RMSE |
|---|---|---|
| Final timestep only | 0.0067 | 0.0086 |
| Final + delta + std (compact) | 0.0053 | 0.0068 |
| Full 12-step sequence (V4) | 0.0052 | 0.0066 |

**Conclusion:** Temporal trajectory information improves prediction.
The full-sequence Transformer is the strongest tested configuration.
The compact representation is close but the full sequence is used in production.

Source: experiments/v4_neural_ablation_report.json

---

## 13. ONNX Export — VALIDATED

**Static ONNX:**

| Property | Value |
|---|---|
| Path | models/edgeresilience/temporal_predictor_v4.onnx |
| Input shape | [1, 12, 17] |
| Output shape | [1] |
| Provider | CPUExecutionProvider |
| Status | VALIDATED |

**Dynamic ONNX:**

| Property | Value |
|---|---|
| Path | models/edgeresilience/temporal_predictor_v4_dynamic.onnx |
| Input shape | [batch, 12, 17] |
| Output shape | [batch] |
| Provider | CPUExecutionProvider |
| Status | VALIDATED |

---

## 14. Dynamic ONNX Numerical Equivalence — VALIDATED

Batch equivalence was verified against PyTorch reference outputs.

| Batch size | Max absolute error | Threshold | Result |
|---|---|---|---|
| 1 | 4.38e-08 | 1e-05 | PASS |
| 4 | 3.54e-08 | 1e-05 | PASS |
| 16 | 5.96e-08 | 1e-05 | PASS |

Source: experiments/v4_dynamic_onnx_equivalence_report.json

---

## 15. CPU Reference Benchmark — VALIDATED

**Environment:** Windows / Intel Core i5-1235U (reference CPU)

| Metric | Value |
|---|---|
| Model format | PyTorch |
| Input shape | [1000, 12, 17] |
| Samples per run | 1,000 |
| Mean batch latency | 29.59 ms |
| Median batch latency | 29.29 ms |
| P95 batch latency | 34.92 ms |
| Throughput | 33,800 samples/sec |

This is a CPU reference measurement. No Snapdragon or accelerator performance
is claimed.

Source: experiments/cpu_reference_benchmark_v4.json

---

## 16. ONNX CPU Benchmark — VALIDATED

Batch-1 comparison between PyTorch and ONNX Runtime on the same CPU:

| Backend | Mean latency | Median latency | P95 latency |
|---|---|---|---|
| PyTorch (CPU) | 1.570 ms | 1.254 ms | 4.558 ms |
| ONNX Runtime (CPU) | 0.267 ms | 0.252 ms | 0.331 ms |
| Speedup (mean) | ~5.88x | — | — |

**This is CPU-to-ONNX evidence on an Intel CPU.**
**This is NOT Snapdragon performance.**
**This is NOT NPU acceleration.**
**This is NOT Qualcomm acceleration.**

Source: experiments/v4_pytorch_vs_onnx_cpu_benchmark.json

---

## 17. Runtime Architecture — VALIDATED

The EdgeResilience V4 runtime implements the full pipeline:

```
V4InferenceEngine          src/ai/v4_inference.py
        |
        v
V4EdgeResilienceRuntime    src/resilience/v4_runtime.py
        |
        +-- interpret_v4_degradation()   src/resilience/v4_risk.py
        |
        +-- evaluate_connectivity()      src/resilience/connectivity.py
        |
        +-- EvidenceBuffer               src/resilience/evidence_buffer.py
        |
        +-- should_synchronize()         src/resilience/connectivity.py
```

---

## 18. Predictive Inference — VALIDATED

The V4InferenceEngine loads the checkpoint, validates the feature contract,
applies stored normalization parameters, and runs the Transformer forward pass.
Output is a scalar predicted future degradation value in [0, 1].

No vehicle actuation occurs. No CAN transmission occurs.

---

## 19. Risk Interpretation — VALIDATED

The V4_DEGRADATION_DEMO_POLICY_V1 maps predicted degradation to risk levels:

| Degradation range | Risk level | Evidence required |
|---|---|---|
| < 0.02 | NORMAL | No |
| 0.02 – 0.04 | LOW | No |
| 0.04 – 0.06 | MEDIUM | Yes |
| 0.06 – 0.07 | HIGH | Yes |
| >= 0.07 | CRITICAL | Yes |

**This policy is a deterministic demonstration policy.**
**It is NOT a certified vehicle safety policy.**
**Thresholds are NOT learned from data.**
**Thresholds are NOT Snapdragon hardware limits.**
**Thresholds are NOT physical vehicle safety limits.**

---

## 20. Connectivity Resilience — VALIDATED

The connectivity module classifies the current network state:

| Condition | State |
|---|---|
| Heartbeat failure OR packet loss >= 80% | DISCONNECTED |
| Packet loss >= 20% OR latency >= 250ms | DEGRADED |
| Otherwise | CONNECTED |

Local inference is always allowed regardless of connectivity state.
Evidence buffering is required when DEGRADED or DISCONNECTED.
Synchronization is allowed only when CONNECTED.

---

## 21. Local Inference — VALIDATED

When connectivity is lost, the V4 model continues to run locally.
Predictions are made from locally available observations.
Evidence is buffered in the local EvidenceBuffer.
No cloud dependency is required for inference.

---

## 22. Evidence Buffering — VALIDATED

The EvidenceBuffer stores bounded, immutable evidence records.
Each record contains:

- UTC timestamp
- event ID
- risk state payload
- telemetry payload
- SHA-256 digest of the canonical record

Records are canonicalized before hashing to ensure deterministic digests.
The buffer is bounded (default 100 records) to prevent unbounded memory growth.

---

## 23. Recovery Detection — VALIDATED

Recovery is detected when connectivity transitions from DISCONNECTED or
DEGRADED to CONNECTED. The runtime tracks the previous connectivity state
and compares it to the current state on each cycle.

---

## 24. Synchronization — VALIDATED (software manifest only)

When recovery is detected and buffered records exist, a synchronization
manifest is prepared. The manifest contains:

- event IDs
- payload digests
- sequence numbers

**This is a software manifest only.**
**No data is transmitted over a real network.**
**No cloud endpoint is contacted.**

---

## 25. Dashboard — VALIDATED

The dashboard is a zero-dependency Python HTTP server serving:

- `/` — HTML dashboard showing V4 demo scenario
- `/api/evidence` — JSON API returning v4_demo_scenario.json

The dashboard displays:
- V4 model name and provenance
- Predicted future degradation per cycle
- Risk level per cycle
- Connectivity state
- Local inference status
- Buffering status
- Recovery detection
- Synchronization readiness
- Evidence count
- Policy name
- Safety boundary footer
- Deployment status (ONNX verified, Snapdragon NOT VERIFIED)

---

## 26. Demo — VALIDATED

The primary competition demo uses V4EdgeResilienceRuntime with the
temporal_predictor_v4.pt checkpoint.

Three-cycle demonstration:

| Cycle | Connectivity | Prediction | Risk | Buffering | Recovery | Sync |
|---|---|---|---|---|---|---|
| cycle-001 | CONNECTED | ~0.0339 | LOW | No | No | No |
| cycle-002 | DISCONNECTED | ~0.0031 | NORMAL | Yes | No | No |
| cycle-003 | CONNECTED | ~0.0436 | MEDIUM | No | Yes | Yes |

Evidence artifact: data/evidence/v4_demo_scenario.json

---

## 27. Provenance Classification

| Artifact | Classification |
|---|---|
| V4 temporal predictor | VALIDATED — new EdgeResilience artifact |
| V4 dataset | VALIDATED — new EdgeResilience synthetic artifact |
| V4 ONNX exports | VALIDATED — new EdgeResilience artifact |
| V4 inference engine | VALIDATED — new EdgeResilience artifact |
| V4 risk policy | VALIDATED — new EdgeResilience artifact |
| V4 runtime | VALIDATED — new EdgeResilience artifact |
| Connectivity module | VALIDATED — new EdgeResilience artifact |
| Evidence buffer | VALIDATED — new EdgeResilience artifact |
| Synchronization module | VALIDATED — new EdgeResilience artifact |
| Dashboard | VALIDATED — new EdgeResilience artifact |
| Vehicle CAN modules | INHERITED/REFERENCE — not used in V4 pipeline |
| HCRL data | INHERITED/REFERENCE — not used as V4 model input |
| Previous CRSS Transformer | INHERITED/REFERENCE — frozen, immutable |
| Snapdragon hardware | PLANNED — NOT VERIFIED |
| Qualcomm QNN | PLANNED — NOT VERIFIED |

---

## 28. Safety Boundary

This project is a software simulation / virtual laboratory.

| Claim | Status |
|---|---|
| Software simulation | YES |
| Synthetic vehicle scenarios | YES |
| Virtual CAN/HIL concepts | YES |
| Physical vehicle testing | NO |
| Production vehicle connection | NO |
| External CAN transmission | NO |
| Direct vehicle actuation | NO |
| Steering control | NO |
| Braking control | NO |
| Throttle control | NO |
| Real emergency dispatch | NO |
| Real public-safety integration | NO |

AI outputs are separated from deterministic safety policy.
AI components do not directly command vehicle actuation.
Risk interpretation is a demonstration policy, not a certified safety control.

---

## 29. Snapdragon Verification Boundary

| Component | Status |
|---|---|
| CPU reference inference | VERIFIED |
| ONNX Runtime CPU inference | VERIFIED |
| ONNX numerical equivalence | VERIFIED |
| Qualcomm QNN execution | NOT VERIFIED |
| Snapdragon hardware deployment | NOT VERIFIED |
| NPU execution | NOT VERIFIED |
| Accelerator utilization | NOT VERIFIED |
| Latency on Snapdragon | NOT VERIFIED |
| Throughput on Snapdragon | NOT VERIFIED |
| Power consumption | NOT VERIFIED |
| Thermal behavior | NOT VERIFIED |

The ~5.88x ONNX CPU speedup is a CPU-to-ONNX measurement on an Intel CPU.
It is NOT a Snapdragon result. It demonstrates ONNX deployment readiness.

The deployment path to Snapdragon is:
ONNX model (validated) -> Qualcomm QNN conversion -> Snapdragon NPU execution

This path is architecturally prepared but not yet hardware-verified.

---

## 30. Limitations

1. V4 dataset is synthetic — not raw vehicle telemetry
2. Risk thresholds are demonstration defaults — not certified safety limits
3. Snapdragon hardware execution not yet verified
4. Synchronization is a software manifest — no real network transmission
5. Single-vehicle scenario — no multi-vehicle cooperative intelligence
6. No real-time streaming input — batch inference from pre-loaded observations
7. CPU training only — no GPU training was performed

---

## 31. Reproducibility

See QUICKSTART.md for the shortest path to reproduce the demo.
See docs/REPRODUCIBILITY.md for full environment and configuration details.

Key commands:

```
python demo/run_demo.py
python scripts/generate_v4_demo_evidence.py
python src/dashboard/server.py
```

---

## 32. Future Roadmap

1. Snapdragon hardware deployment and QNN conversion (P0 for hardware phase)
2. V2X Agentic AI Cooperative Cyber Resilience (future major expansion)
3. Multi-vehicle cooperative threat detection
4. Geographic threat clustering
5. Mock city/public-safety alert interface (simulation only)
6. Real-time streaming inference pipeline
7. Quantization and distillation for edge efficiency
