# EdgeResilience — 10: Competition Presentation

**Qualcomm Snapdragon AI Lab Build and Present Challenge**
**Project:** EdgeResilience: Snapdragon-Powered Predictive Intelligence
for Connected Vehicle Safety

---

## The One Sentence That Defines This Submission

> EdgeResilience is designed for on-device deployment on
> Snapdragon-powered HP PCs. The current validated implementation
> establishes the V4 predictive model, ONNX deployment artifact,
> local inference architecture, and reproducible software
> demonstration. Snapdragon hardware and Qualcomm QNN execution
> remain explicitly unverified until tested on the target platform.

---

## Evaluation Category 1: Technical Implementation

### What was built and validated

**V4 Temporal Transformer** — EdgeResilienceTemporalPredictor
- 71,170 parameters
- 17 cyber features × 12 observation steps
- Learned temporal attention pooling
- Output: predicted_future_degradation ∈ [0, 1]
- Test MAE: 0.0051 | Test RMSE: 0.0066 | Beats mean baseline by 75%

**Temporal ablation confirms the design choice:**
Full 12-step sequence achieves MAE 0.0052 vs 0.0067 for final-step-only.
Temporal trajectory information provides measurable improvement.

**Complete resilience pipeline:**
- Deterministic risk interpretation (V4_DEGRADATION_DEMO_POLICY_V1)
- Connectivity state evaluation (CONNECTED / DEGRADED / DISCONNECTED)
- Local inference — always active, no cloud dependency
- Evidence buffer — SHA-256 hashed, bounded, tamper-evident
- Recovery detection — DISCONNECTED → CONNECTED transition
- Synchronization manifest — ordered, verifiable evidence chain

**ONNX deployment:**
- Dynamic ONNX export validated across batch sizes 1, 4, 16
- Max numerical error: 5.96e-08 (threshold 1e-5, margin 168×)
- ONNX Runtime CPU: ~5.88× lower latency vs PyTorch (CPU-to-CPU)

**Everything above is validated with reproducible evidence artifacts.**

---

## Evaluation Category 2: Application Use Case and Innovation

### The real-world problem

Connected vehicles face cyber threats that can degrade safety-critical
systems. The challenge is not just detection — it is **local, predictive,
resilient intelligence** that operates entirely on-device, without cloud
dependency, even during connectivity loss.

### Why this is innovative

**1. Predictive, not reactive.**
The V4 model predicts *future* degradation from a temporal trajectory
of cyber telemetry. It gives the system time to prepare before a threat
materializes — not just react after the fact.

**2. Complete resilience lifecycle.**
Most edge AI demos show a model making a prediction. EdgeResilience
shows a complete lifecycle: prediction → risk → connectivity loss →
local continuity → evidence preservation → recovery → synchronization.
This is a differentiated architecture.

**3. Tamper-evident evidence chain.**
Every risk event produces a SHA-256 hashed, timestamped evidence record.
The synchronization manifest provides an ordered, verifiable chain of
custody — auditable after the fact. This is an engineering-grade
evidence system, not a demo artifact.

**4. Edge-first design.**
The model is deliberately compact (71K parameters) with a fixed input
shape and standard ONNX operations. It is designed around the constraints
of edge inference on a Snapdragon-powered platform — not a large model
hoping to fit on a device.

### The use case narrative

A Snapdragon-powered vehicle compute module runs EdgeResilience
continuously. When cyber telemetry indicates rising degradation, the
system raises the risk level and begins buffering evidence. If the
vehicle enters a dead zone and loses connectivity, inference continues
locally. When connectivity recovers, the buffered evidence is
synchronized to the infrastructure backend for forensic analysis.

This is a complete, end-to-end edge AI resilience story.

---

## Evaluation Category 3: Deployment and Accessibility

### Current deployment status

| Backend | Status |
|---|---|
| CPU reference (PyTorch) | VERIFIED |
| ONNX Runtime (CPU) | VERIFIED — ~5.88× vs PyTorch |
| Snapdragon X Elite | VERIFIED — COMPONENT / WORKLOAD |
| Qualcomm QNN / HTP | VERIFIED — COMPONENT / WORKLOAD |
| HTP profiling | VERIFIED — 97.22% utilization |
| Full CPU ↔ Snapdragon numerical equivalence | NOT VERIFIED |
| Physical vehicle | NOT PERFORMED |

### The Snapdragon deployment path is real and specific

```
ONNX model (validated, dynamic batch)
        │
        ▼
Qualcomm AI Hub QNN / HTP compilation
        │
        ▼
Snapdragon X Elite CRD target execution
        │
        ▼
HTP profiling and performance evidence
```

This is not a hypothetical Snapdragon path. Component and workload-level
execution has been demonstrated on a Snapdragon X Elite CRD through
Qualcomm QNN/HTP. The remaining limitation is full production-model
CPU-to-Snapdragon numerical equivalence.

### Why the model is well-suited for NPU acceleration

- 71,170 parameters — fits comfortably in NPU memory
- Fixed input shape [batch, 12, 17] — enables static NPU graph compilation
- Standard ONNX ops only — Linear, LayerNorm, GELU, Softmax, Sigmoid
- No dynamic control flow — ideal for NPU execution
- HTP profiling has measured 97.22% HTP utilization for the validated
  temporal-pooling + prediction-head workload
- The profiled workload reports an estimated 36 µs inference time
- These measurements are workload-specific and are not claimed as
  full V4 system latency or acceleration vs CPU

### Accessibility

- Single command to run the demo: `python demo\run_demo.py`
- Single command for dashboard: `python src\dashboard\server.py`
- Zero external dependencies for the dashboard (Python stdlib only)
- All evidence artifacts are JSON — human-readable and machine-parseable
- Full reproducibility documentation with exact checksums

---

## Evaluation Category 4: Presentation and Documentation

### Documentation produced

14 documents covering every aspect of the submission:

| Document | Purpose |
|---|---|
| README.md | Project overview with exact commands |
| QUICKSTART.md | 5-command path to reproduce everything |
| docs/FINAL_TECHNICAL_BASELINE.md | Complete technical reference |
| docs/architecture/ARCHITECTURE.md | Full pipeline diagrams |
| docs/REPRODUCIBILITY.md | Environment, checksums, configuration |
| docs/EVIDENCE_INDEX.md | All evidence artifacts indexed |
| docs/SNAPDRAGON_DEPLOYMENT.md | Deployment status and path |
| docs/COMPETITION_CLAIMS.md | Allowed/disallowed wording per claim |
| docs/SAFETY_BOUNDARY.md | Explicit safety boundary |
| docs/MODEL_CARD_V4.md | Model card |
| docs/DATA_CARD_V4.md | Dataset card |
| docs/EXPERIMENT_SUMMARY.md | All experiment results |
| docs/submission/ | This submission package (10 documents) |
| docs/presentation/ | Demo narrative + competition narrative |

### Evidence-backed claims

Every claim in this submission is backed by a specific artifact:

| Claim | Evidence artifact |
|---|---|
| MAE 0.0051 | temporal_predictor_v4_report.json |
| Temporal ablation | v4_neural_ablation_report.json |
| ONNX equivalence | v4_dynamic_onnx_equivalence_report.json |
| ~5.88× ONNX speedup | v4_pytorch_vs_onnx_cpu_benchmark.json |
| Three-cycle demo | v4_demo_scenario.json |
| Deployment status | snapdragon_deployment_manifest_v4.json |

### Honest boundaries prevent overclaiming

The COMPETITION_CLAIMS.md document explicitly defines allowed and
disallowed wording for every major claim. This prevents accidental
overclaiming during presentation and demonstrates engineering integrity.

---

## Summary: What EdgeResilience Delivers

| Dimension | Delivered |
|---|---|
| Real problem | Connected vehicle cyber-physical resilience |
| Working AI | V4 Temporal Transformer, validated, reproducible |
| Edge deployment | ONNX export, CPU + ONNX verified |
| Snapdragon path | Specific, documented, QNN-ready |
| Innovation | Complete resilience lifecycle, not just a model |
| Evidence | 10+ validated artifacts with checksums |
| Documentation | 14 documents, all consistent |
| Honesty | Explicit NOT VERIFIED where hardware is absent |

---

## Remaining Roadmap

1. **Complete Snapdragon numerical validation** — resolve operator-level
   CPU-to-Snapdragon divergence and establish full production-model
   numerical equivalence before making an end-to-end equivalence claim.

2. **Extended Snapdragon benchmarking** — measure complete production-graph
   latency, throughput, memory, power and thermal behavior under a clearly
   defined benchmark protocol.

2. **V2X Agentic AI Cooperative Cyber Resilience** — multi-vehicle
   cooperative threat detection, geographic clustering, mock city
   safety interface (simulation only)

3. **Real-time streaming inference** — continuous inference from a
   simulated telemetry stream

4. **Quantization and distillation** — further model compression
   for more efficient NPU deployment
