# EdgeResilience

## Snapdragon-Powered Predictive Intelligence for Connected Vehicle Safety

**Competition:** Qualcomm Snapdragon AI Lab Build and Present Challenge
**Status:** Competition ready — V4 baseline + Snapdragon component/workload validation

---

## Problem

Connected vehicles face cyber threats including CAN bus anomalies, message
injection, timing manipulation, and payload tampering. When a vehicle loses
connectivity to a cloud or infrastructure backend, it must continue to operate
safely using only local compute. Evidence of anomalous behavior must be
preserved locally and synchronized when connectivity recovers.

Three dimensions:

1. **Predictive** — detect degradation before it becomes critical
2. **Resilient** — maintain local intelligence when connectivity is lost
3. **Auditable** — preserve tamper-evident evidence for post-event analysis

---

## Solution

EdgeResilience is a complete edge AI pipeline that:

1. Accepts 17 cyber telemetry features over 12 temporal observation steps
2. Runs a Temporal Transformer to predict future resilience degradation
3. Applies a deterministic risk interpretation policy
4. Evaluates connectivity state
5. Maintains local inference regardless of connectivity
6. Buffers SHA-256 hashed evidence records when connectivity is degraded
7. Detects connectivity recovery
8. Prepares a synchronization manifest when recovery is confirmed

The model is exported to ONNX for deployment. Qualcomm AI Hub has been
used to compile and execute a validated V4 workload on a Snapdragon X Elite
CRD through Qualcomm QNN/HTP. HTP profiling has also been completed.
Full CPU-to-Snapdragon numerical equivalence remains under investigation.

---

## Architecture

```
Vehicle/Cyber Observations (17 features x 12 steps)
        |
        v
V4 Temporal Predictor (EdgeResilienceTemporalPredictor)
        |
        v
Predicted Future Degradation
        |
        v
Deterministic Risk Interpretation (V4_DEGRADATION_DEMO_POLICY_V1)
        |
        v
Connectivity State Evaluation
        |
        +---> Local Inference (always active)
        +---> Evidence Buffer (when degraded/disconnected)
        +---> Recovery Detection
        |
        v
Synchronization Manifest (software only)
        |
        v
Auditable Evidence
```

See [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md) for the full diagram.

---

## V4 Model

| Property | Value |
|---|---|
| Name | EdgeResilience_V4_TemporalPredictor |
| Architecture | Temporal Transformer |
| Input | 17 features x 12 steps |
| Output | predicted_future_degradation (scalar, 0-1) |
| d_model | 64 |
| Attention heads | 4 |
| Transformer layers | 2 |
| Feed-forward dim | 128 |
| Parameters | 71,170 |
| Test MAE | ~0.0051 |
| Test RMSE | ~0.0066 |
| Checkpoint | models/edgeresilience/temporal_predictor_v4.pt |

The temporal ablation confirmed that the full 12-step sequence outperforms
both final-step-only and compact summary representations.

---

## Dataset

| Property | Value |
|---|---|
| Path | data/processed/temporal/edgeresilience_temporal_dataset_v4.jsonl |
| Records | 5,000 |
| Features | 17 per step |
| Steps | 12 |
| Generation | Synthetic EdgeResilience temporal scenarios |
| SHA256 | 02a82f0f5ee78dc4e3be28b81b53b6eb4eb884600a4734f3eb3aaa279cb3a911 |

The dataset uses synthetic cyber-physical scenario features. Raw HCRL
measurements are NOT the direct model input.

---

## Validation

| Experiment | Result | Evidence |
|---|---|---|
| V4 training | MAE 0.0051, RMSE 0.0066 | models/edgeresilience/temporal_predictor_v4_report.json |
| Temporal ablation | Full sequence best | experiments/v4_neural_ablation_report.json |
| ONNX static equivalence | PASS | experiments/v4_onnx_equivalence_report.json |
| ONNX dynamic equivalence | PASS (max error 5.96e-08) | experiments/v4_dynamic_onnx_equivalence_report.json |
| CPU benchmark | 33,800 samples/sec | experiments/cpu_reference_benchmark_v4.json |
| ONNX CPU speedup | ~5.99x vs PyTorch (CPU-to-CPU) | experiments/v4_pytorch_vs_onnx_cpu_benchmark.json |
| Three-cycle demo | PASS | data/evidence/v4_demo_scenario.json |

---

## Demo

The primary competition demo uses `V4EdgeResilienceRuntime` with the
validated `temporal_predictor_v4.pt` checkpoint.

```
python demo/run_demo.py
```

Three-cycle scenario:

| Cycle | Connectivity | Degradation | Risk | Buffering | Recovery | Sync |
|---|---|---|---|---|---|---|
| cycle-001 | CONNECTED | ~0.0339 | LOW | No | No | No |
| cycle-002 | DISCONNECTED | ~0.0031 | NORMAL | Yes | No | No |
| cycle-003 | CONNECTED | ~0.0436 | MEDIUM | No | Yes | Yes |

---

## Dashboard

```
python src/dashboard/server.py
```

Open: http://127.0.0.1:8765

The dashboard displays the V4 demo scenario with:
- Predicted future degradation per cycle
- Risk level with color coding
- Connectivity state
- Local inference / buffering / recovery / sync status
- Model provenance and policy name
- Deployment status (ONNX verified, Snapdragon component/workload validated)
- Safety boundary footer

---

## Deployment

| Backend | Status |
|---|---|
| CPU reference (PyTorch) | VERIFIED |
| ONNX Runtime (CPU) | VERIFIED |
| Qualcomm QNN / HTP | VERIFIED — COMPONENT / WORKLOAD |
| Snapdragon X Elite | VERIFIED — COMPONENT / WORKLOAD |
| HTP profiling | VERIFIED — VALIDATED WORKLOAD |
| Full CPU ↔ Snapdragon numerical equivalence | NOT VERIFIED |

Qualcomm QNN / HTP execution has been validated on a Snapdragon X Elite
CRD for the tested V4 workload. The profiled workload achieved an estimated
36 µs inference time and 97.22% HTP utilization.

These are workload-specific measurements and are not full vehicle-system
latency measurements. The ~5.99x ONNX speedup is a CPU-to-CPU measurement
on an Intel Core i5-1235U and is NOT a Snapdragon result.

Full CPU-to-Snapdragon numerical equivalence remains NOT VERIFIED.

See [docs/SNAPDRAGON_DEPLOYMENT.md](docs/SNAPDRAGON_DEPLOYMENT.md) for details.

---

## Safety Boundary

This project is a **software simulation / virtual laboratory**.

- Physical vehicle testing: **NO**
- Production vehicle connection: **NO**
- External CAN transmission: **NO**
- Direct vehicle actuation: **NO**
- Real emergency dispatch: **NO**

See [docs/SAFETY_BOUNDARY.md](docs/SAFETY_BOUNDARY.md).

---

## Reproducibility

See [QUICKSTART.md](QUICKSTART.md) for the fastest path to run the demo.

Requirements: Python 3.9+, PyTorch, ONNX Runtime, NumPy, scikit-learn

```
pip install torch onnxruntime numpy scikit-learn joblib
```

---

## Directory Structure

```
EdgeResilience/
  demo/                     Competition demo runner
  docs/                     Documentation
    architecture/           Architecture diagrams
    presentation/           Competition presentation materials
    provenance/             Provenance register and manifest
  data/
    evidence/               Demo evidence artifacts
    processed/temporal/     V4 dataset
  experiments/              Experiment reports and benchmarks
  models/edgeresilience/    V4 checkpoint and ONNX exports
  scripts/                  Training, validation, benchmark scripts
  src/
    ai/                     V4 inference engine and model
    dashboard/              Zero-dependency HTTP dashboard
    resilience/             Runtime, risk, connectivity, evidence
    snapdragon/             Deployment manifest module
    vehicle/                Inherited CAN/HIL reference modules
  inherited/                Previous project (reference only)
```

---

## Limitations

1. V4 dataset is synthetic — not raw vehicle telemetry
2. Risk thresholds are demonstration defaults — not certified safety limits
3. Full CPU-to-Snapdragon numerical equivalence remains under investigation
4. Synchronization is a software manifest — no real network transmission
5. Single-vehicle scenario only

---

## Future Roadmap

1. Resolve CPU-to-Snapdragon numerical divergence and complete full-model validation
2. V2X Agentic AI Cooperative Cyber Resilience (multi-vehicle simulation)
3. Geographic threat clustering
4. Mock city/public-safety alert interface (simulation only)

---

## Project Separation

The previous project (Predictive Cyber-Physical Resilience) is retained under
`inherited/Predictive-Cyber-Physical-Resilience/` as reference material only.

EdgeResilience has its own source code, models, datasets, evidence, and
Git history. Inherited material is explicitly classified before any reuse.

See [docs/provenance/PROVENANCE_REGISTER.md](docs/provenance/PROVENANCE_REGISTER.md).
