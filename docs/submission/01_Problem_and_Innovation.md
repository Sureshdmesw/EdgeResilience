# EdgeResilience — 01: Problem and Innovation

## The Problem

Connected vehicles are increasingly exposed to cyber threats:
CAN bus message injection, timing manipulation, payload tampering,
and anomalous traffic patterns that degrade safety-critical systems.

The challenge is not just detection. It is **local, predictive, resilient
intelligence** — operating entirely on-device, without cloud dependency,
even when the vehicle loses network connectivity.

Three dimensions define the problem:

| Dimension | Challenge |
|---|---|
| Predictive | Detect degradation *before* it becomes critical, not after |
| Resilient | Maintain local intelligence when connectivity is lost |
| Auditable | Preserve tamper-evident evidence for post-event analysis |

Existing approaches are largely reactive and cloud-dependent.
EdgeResilience addresses all three dimensions at the edge.

---

## Why This Problem Matters for Snapdragon

Qualcomm Snapdragon AI PCs are built around a dedicated NPU for
local AI processing. The EdgeResilience workload is a natural fit:

- Always-on temporal inference from a compact model (71K parameters)
- No cloud round-trip required for prediction
- Local evidence buffering during connectivity loss
- Recovery and synchronization when connectivity restores

This is precisely the class of workload that benefits from
Snapdragon's on-device AI architecture: low latency, low power,
always available, privacy-preserving.

---

## The Innovation

EdgeResilience is not a single model. It is a complete **edge AI
resilience pipeline** with five validated components working together:

```
Temporal Prediction
      ↓
Deterministic Risk Interpretation
      ↓
Connectivity-Aware Resilience
      ↓
Local Evidence Buffering
      ↓
Recovery + Synchronization
```

Each component is independently validated and the full pipeline
is demonstrated end-to-end in a reproducible three-cycle scenario.

### Innovation 1: Temporal Predictive Intelligence

The V4 Temporal Transformer captures **degradation trajectories**
over 12 observation steps — not just instantaneous anomaly scores.

Ablation evidence confirms temporal trajectory information provides
measurable improvement over single-step input:

| Input | MAE | Improvement |
|---|---|---|
| Final timestep only | 0.0067 | baseline |
| Full 12-step sequence | 0.0052 | +22% |

### Innovation 2: Connectivity-Aware Resilience Lifecycle

The system implements a complete resilience lifecycle:

```
CONNECTED → inference active, sync allowed
     ↓ (connectivity lost)
DISCONNECTED → inference continues locally, evidence buffered
     ↓ (connectivity recovers)
CONNECTED → recovery detected, sync manifest prepared
```

This is a differentiated architecture beyond "here is an AI model."

### Innovation 3: Tamper-Evident Evidence Chain

Every risk event produces a SHA-256 hashed, UTC-timestamped
evidence record. The synchronization manifest provides an ordered,
verifiable chain of custody — auditable after the fact.

### Innovation 4: Edge-First Design for Snapdragon

The model is deliberately compact:

- 71,170 parameters
- 17 features × 12 steps input
- ONNX exported with dynamic batch support
- Numerically equivalent to PyTorch reference (max error 5.96e-08)
- ~5.88x lower latency with ONNX Runtime vs PyTorch (CPU-to-CPU)

This is not a large model hoping to fit on a device.
It is a model **designed around the constraints of edge inference**
on a Snapdragon-powered platform.

---

## What This Is Not

- Not a cloud-dependent system
- Not a reactive anomaly detector
- Not a physical vehicle test
- Not a certified safety system

It is a **software demonstration of edge AI predictive intelligence**,
designed for Snapdragon deployment, with a clear and honest path
from current validated state to target hardware execution.
