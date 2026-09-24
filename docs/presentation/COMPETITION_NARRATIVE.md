# EdgeResilience — Competition Presentation

**Competition:** Qualcomm Snapdragon AI Lab Build and Present Challenge
**Project:** EdgeResilience: Snapdragon-Powered Predictive Intelligence for Connected Vehicle Safety

---

## Evaluation Category 1: Technical Implementation

### What was built

A complete edge AI pipeline with five validated components:

1. **V4 Temporal Predictor** — EdgeResilienceTemporalPredictor
   - Temporal Transformer: 2 layers, 4 heads, d_model=64, ff=128
   - Input: 17 cyber features x 12 observation steps
   - Output: predicted_future_degradation (scalar, 0-1)
   - Learned temporal attention pooling
   - 71,170 parameters
   - Test MAE: 0.0051 | Test RMSE: 0.0066

2. **Deterministic Risk Interpretation** — V4_DEGRADATION_DEMO_POLICY_V1
   - Maps predicted degradation to NORMAL/LOW/MEDIUM/HIGH/CRITICAL
   - Deterministic — not learned, not certified safety limits
   - Evidence-required flag triggers local buffering

3. **Connectivity Resilience Runtime** — V4EdgeResilienceRuntime
   - Evaluates connectivity: CONNECTED / DEGRADED / DISCONNECTED
   - Local inference always active regardless of connectivity
   - Evidence buffering when degraded or disconnected

4. **Evidence Buffer** — EvidenceBuffer
   - SHA-256 hashed, UTC-timestamped records
   - Bounded (100 records), canonicalized JSON
   - Tamper-evident local storage

5. **Synchronization Manifest** — synchronization.py
   - Detects DISCONNECTED -> CONNECTED recovery transition
   - Prepares ordered manifest of buffered evidence
   - Software manifest only — no network transmission

### Validation evidence

| Experiment | Result |
|---|---|
| V4 training | MAE 0.0051, RMSE 0.0066, beats mean baseline |
| Temporal ablation | Full sequence best (0.0052 vs 0.0067 final-only) |
| ONNX dynamic equivalence | PASS — max error 5.96e-08 across batch 1/4/16 |
| CPU benchmark | 33,800 samples/sec |
| ONNX CPU speedup | ~5.88x vs PyTorch (CPU-to-CPU) |
| Three-cycle demo | PASS — connected, disconnected, recovery |

---

## Evaluation Category 2: Application Use Case and Innovation

### Real-world problem

Connected vehicles face cyber threats that can degrade safety-critical
systems. Existing approaches are reactive. EdgeResilience is predictive:
it forecasts future degradation from temporal cyber telemetry trajectories,
enabling proactive resilience before a threat becomes critical.

### Innovation

1. **Temporal prediction** — 12-step Transformer captures degradation
   trajectories, not just instantaneous anomalies. Ablation confirms
   temporal information provides measurable improvement.

2. **Connectivity-aware resilience** — the system degrades gracefully.
   When connectivity is lost, inference continues locally. Evidence is
   preserved. When connectivity recovers, synchronization is prepared.
   This is a complete resilience lifecycle, not just detection.

3. **Auditable evidence chain** — every risk event produces a SHA-256
   hashed, timestamped evidence record. The synchronization manifest
   provides an ordered, verifiable chain of custody.

4. **Edge-first design** — the model is small (71K parameters), ONNX-exported,
   and designed for Snapdragon NPU deployment. The architecture is
   appropriate for always-on edge vehicle compute.

### Use case

A Snapdragon-powered vehicle compute module runs EdgeResilience continuously.
When cyber telemetry indicates rising degradation, the system raises the
risk level and begins buffering evidence. If the vehicle enters a tunnel
or dead zone and loses connectivity, inference continues locally. When
connectivity recovers, the buffered evidence is synchronized to the
infrastructure backend for forensic analysis.

---

## Evaluation Category 3: Deployment and Accessibility

### Current deployment status

| Backend | Status |
|---|---|
| CPU reference (PyTorch) | VERIFIED |
| ONNX Runtime (CPU) | VERIFIED |
| Qualcomm QNN | NOT VERIFIED — pending hardware |
| Snapdragon NPU | NOT VERIFIED — pending hardware |

### ONNX deployment

The V4 model is exported to ONNX with dynamic batch support.
Numerical equivalence is verified across batch sizes 1, 4, and 16.
The ONNX model is the deployment artifact for QNN conversion.

### CPU performance (reference measurement)

- ONNX Runtime mean latency: 0.267 ms (batch-1, Intel Core i5-1235U)
- ~5.88x improvement vs PyTorch on the same CPU
- This is a CPU-to-CPU measurement — NOT a Snapdragon result

### Snapdragon deployment path

```
ONNX model (validated)
    -> Qualcomm QNN conversion (qnn-onnx-converter)
    -> Snapdragon NPU execution
    -> Edge deployment on vehicle compute module
```

The model size (71K parameters) and architecture (small Transformer)
are well-suited for NPU acceleration. The expected benefits are:
lower latency, lower power, and thermal efficiency for always-on operation.

Hardware verification is pending an actual Snapdragon device.

### Accessibility

- Zero external dependencies for the dashboard (Python stdlib HTTP server)
- Single command to run the demo: `python demo\run_demo.py`
- Single command to start the dashboard: `python src\dashboard\server.py`
- All evidence artifacts are JSON — human-readable and machine-parseable
- Full reproducibility documentation in docs/REPRODUCIBILITY.md

---

## Evaluation Category 4: Presentation and Documentation

### Documentation produced

| Document | Purpose |
|---|---|
| README.md | Project overview, architecture, validation, commands |
| QUICKSTART.md | Fastest path to run the demo |
| docs/FINAL_TECHNICAL_BASELINE.md | Complete technical reference |
| docs/architecture/ARCHITECTURE.md | System architecture with ASCII diagrams |
| docs/REPRODUCIBILITY.md | Environment, checksums, configuration |
| docs/EVIDENCE_INDEX.md | Index of all evidence artifacts |
| docs/SNAPDRAGON_DEPLOYMENT.md | Deployment status and path |
| docs/COMPETITION_CLAIMS.md | Allowed/disallowed wording for every claim |
| docs/SAFETY_BOUNDARY.md | Explicit safety boundary statement |
| docs/provenance/PROVENANCE_REGISTER.md | Artifact classification |
| docs/MODEL_CARD_V4.md | Model card |
| docs/DATA_CARD_V4.md | Dataset card |

### Evidence chain

Every claim in this submission is backed by a specific evidence artifact:

- Training metrics -> temporal_predictor_v4_report.json
- Temporal ablation -> v4_neural_ablation_report.json
- ONNX equivalence -> v4_dynamic_onnx_equivalence_report.json
- CPU benchmark -> cpu_reference_benchmark_v4.json
- ONNX speedup -> v4_pytorch_vs_onnx_cpu_benchmark.json
- Demo behavior -> v4_demo_scenario.json
- Deployment status -> snapdragon_deployment_manifest_v4.json

### Honest boundaries

This submission explicitly states:

- Snapdragon hardware: NOT VERIFIED
- Qualcomm QNN: NOT VERIFIED
- Physical vehicle testing: NOT PERFORMED
- The ~5.88x speedup is CPU-to-CPU, not Snapdragon

These boundaries are documented in COMPETITION_CLAIMS.md and
SAFETY_BOUNDARY.md to prevent accidental overclaiming.

---

## Future Roadmap

1. **Snapdragon hardware verification** — QNN conversion, NPU execution,
   latency/power/thermal measurement on actual Snapdragon device

2. **V2X Agentic AI Cooperative Cyber Resilience** — multi-vehicle
   cooperative threat detection, geographic clustering, mock city
   safety interface (simulation only)

3. **Real-time streaming inference** — replace batch demo with
   continuous inference from a simulated telemetry stream

4. **Quantization and distillation** — reduce model size further
   for more efficient NPU deployment

---

## Summary

EdgeResilience delivers a validated, reproducible, evidence-backed
edge AI pipeline for connected vehicle cyber-physical safety.

The V4 baseline is validated. The ONNX deployment is verified.
The Snapdragon path is architecturally prepared and ready for
hardware verification.

The project is honest about what has been measured and what has not.
