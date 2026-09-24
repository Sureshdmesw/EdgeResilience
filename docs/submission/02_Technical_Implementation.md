# EdgeResilience — 02: Technical Implementation

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  INPUT: 17 cyber features × 12 temporal observation steps   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  V4 TEMPORAL TRANSFORMER                                     │
│  EdgeResilienceTemporalPredictor                             │
│                                                             │
│  Input projection:  Linear(17 → 64)                         │
│  Positional embed:  Learned [1, 12, 64]                     │
│  Encoder:           2 layers, 4 heads, ff=128               │
│  Attention pool:    Learned per-step weights                 │
│  Output head:       LayerNorm → Linear → GELU → Sigmoid     │
│                                                             │
│  Output: predicted_future_degradation ∈ [0, 1]              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  DETERMINISTIC RISK INTERPRETATION                           │
│  V4_DEGRADATION_DEMO_POLICY_V1                               │
│                                                             │
│  < 0.02  → NORMAL    0.04–0.06 → MEDIUM                     │
│  0.02–0.04 → LOW     0.06–0.07 → HIGH    ≥ 0.07 → CRITICAL  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  CONNECTIVITY STATE EVALUATION                               │
│  CONNECTED / DEGRADED / DISCONNECTED                         │
└─────────────────────────────────────────────────────────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        Local          Evidence       Recovery
        Inference      Buffer         Detection
        (always)       (when          (DISCONNECTED
                       degraded)      → CONNECTED)
                            │             │
                            └──────┬──────┘
                                   ▼
                        Synchronization Manifest
                        (software — no network tx)
```

---

## Component Inventory

| Component | File | Status |
|---|---|---|
| Temporal predictor architecture | src/ai/temporal_predictor.py | VALIDATED |
| V4 inference engine | src/ai/v4_inference.py | VALIDATED |
| V4 risk interpretation | src/resilience/v4_risk.py | VALIDATED |
| V4 edge runtime | src/resilience/v4_runtime.py | VALIDATED |
| Connectivity policy | src/resilience/connectivity.py | VALIDATED |
| Evidence buffer | src/resilience/evidence_buffer.py | VALIDATED |
| Synchronization manifest | src/resilience/synchronization.py | VALIDATED |
| Dashboard server | src/dashboard/server.py | VALIDATED |
| Snapdragon deployment module | src/snapdragon/deployment.py | VALIDATED |

---

## V4 Model Specification

| Property | Value |
|---|---|
| Architecture | Temporal Transformer |
| Parameters | 71,170 |
| Input | [batch, 12, 17] float32 |
| Output | [batch] float32, Sigmoid |
| d_model | 64 |
| Attention heads | 4 |
| Transformer layers | 2 |
| Feed-forward dim | 128 |
| Pooling | Learned temporal attention |
| Checkpoint | models/edgeresilience/temporal_predictor_v4.pt |
| Checkpoint SHA256 | b551ad9f02b56668ef3f8f7873133748275307f1934ec7fd77da14e7325d26b9 |

---

## Training and Validation

| Metric | Value |
|---|---|
| Test MAE | 0.0051 |
| Test RMSE | 0.0066 |
| Mean baseline MAE | 0.0203 |
| Beats baseline | YES (+75% improvement) |
| Best epoch | 77 / 80 |
| Best validation loss | 4.378e-05 |
| Random seed | 42 |
| Train / val / test | 3,200 / 800 / 1,000 |

---

## Temporal Ablation Evidence

| Input representation | MAE | RMSE |
|---|---|---|
| Final timestep only | 0.0067 | 0.0086 |
| Final + delta + std | 0.0053 | 0.0068 |
| Full 12-step sequence (V4) | 0.0052 | 0.0066 |

Temporal trajectory information provides measurable improvement.
The full-sequence Transformer is the strongest tested configuration.

Source: experiments/v4_neural_ablation_report.json

---

## AI / Deterministic Separation

A key architectural decision: AI outputs are **never directly wired
to safety-critical state transitions**.

```
AI Layer (probabilistic)
  predicted_future_degradation: float
        │
        │  ← boundary
        ▼
Deterministic Policy Layer
  risk_level: categorical
  evidence_required: boolean
        │
        │  ← boundary
        ▼
Resilience State Layer
  local_inference_allowed
  local_buffering_required
  recovery_detected
  synchronization_ready
```

This separation is intentional and important for any safety-adjacent
edge AI system. The model informs; deterministic logic decides.

---

## Evidence Buffer Design

Each evidence record contains:

- UTC timestamp (software clock)
- Event ID
- Risk state payload
- Telemetry payload
- SHA-256 digest of the canonical record

Records are canonicalized before hashing (sorted keys, deterministic
JSON serialization) to ensure digest reproducibility.

The buffer is bounded (100 records) to prevent unbounded memory growth
on a constrained edge device — a deliberate edge-deployment consideration.

---

## Dataset

| Property | Value |
|---|---|
| Records | 5,000 |
| Features per step | 17 |
| Observation steps | 12 |
| Target | future_degradation (continuous) |
| Generation | Synthetic EdgeResilience temporal scenarios |
| SHA256 | 02a82f0f5ee78dc4e3be28b81b53b6eb4eb884600a4734f3eb3aaa279cb3a911 |

The dataset uses synthetic cyber-physical scenario features.
Raw HCRL measurements are NOT the direct model input.
