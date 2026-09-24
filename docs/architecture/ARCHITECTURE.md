# EdgeResilience — System Architecture

**Project:** EdgeResilience: Snapdragon-Powered Predictive Intelligence for Connected Vehicle Safety
**Status:** VALIDATED (CPU + ONNX) | Snapdragon deployment: PENDING

---

## Overview

EdgeResilience is a complete edge AI pipeline for connected vehicle
cyber-physical safety. It predicts future resilience degradation from
temporal cyber telemetry, maintains local intelligence during connectivity
loss, buffers tamper-evident evidence, and prepares synchronization when
connectivity recovers.

---

## Full System Architecture

```
+------------------------------------------------------------------+
|              VEHICLE / CYBER OBSERVATIONS                        |
|                                                                  |
|  17 cyber features x 12 temporal observation steps              |
|  (synthetic EdgeResilience scenario representation)              |
+------------------------------------------------------------------+
                            |
                            v
+------------------------------------------------------------------+
|              V4 TEMPORAL PREDICTOR                               |
|              EdgeResilienceTemporalPredictor                     |
|                                                                  |
|  Input projection: 17 -> d_model=64                             |
|  Positional embedding: [1, 12, 64]                              |
|  Transformer encoder: 2 layers, 4 heads, ff=128                 |
|  Temporal attention pooling: learned per-step weights           |
|  Output head: LayerNorm -> Linear(64,32) -> GELU -> Linear(32,1)|
|  Activation: Sigmoid -> predicted_future_degradation [0,1]      |
|                                                                  |
|  Checkpoint: models/edgeresilience/temporal_predictor_v4.pt     |
|  Parameters: 71,170                                             |
|  Test MAE: ~0.0051  |  Test RMSE: ~0.0066                       |
+------------------------------------------------------------------+
                            |
                            v  predicted_future_degradation
+------------------------------------------------------------------+
|              DETERMINISTIC RISK INTERPRETATION                   |
|              V4_DEGRADATION_DEMO_POLICY_V1                       |
|                                                                  |
|  < 0.02  -> NORMAL   (no evidence required)                     |
|  0.02-0.04 -> LOW    (no evidence required)                     |
|  0.04-0.06 -> MEDIUM (evidence required)                        |
|  0.06-0.07 -> HIGH   (evidence required)                        |
|  >= 0.07 -> CRITICAL (evidence required)                        |
|                                                                  |
|  NOT a certified vehicle safety policy                          |
|  NOT learned thresholds                                         |
|  NOT Snapdragon hardware limits                                 |
+------------------------------------------------------------------+
                            |
                            v  risk_level + evidence_required
+------------------------------------------------------------------+
|              CONNECTIVITY STATE EVALUATION                       |
|                                                                  |
|  heartbeat_failure OR packet_loss >= 80% -> DISCONNECTED        |
|  packet_loss >= 20% OR latency >= 250ms  -> DEGRADED            |
|  otherwise                               -> CONNECTED           |
+------------------------------------------------------------------+
                            |
              +-------------+-------------+
              |                           |
              v                           v
+------------------------+   +---------------------------+
|  LOCAL INFERENCE       |   |  EVIDENCE BUFFER          |
|  (always active)       |   |  (when risk >= MEDIUM     |
|                        |   |   or connectivity         |
|  V4 model runs         |   |   degraded/disconnected)  |
|  regardless of         |   |                           |
|  connectivity state    |   |  SHA-256 hashed records   |
|                        |   |  UTC timestamped          |
|  No cloud dependency   |   |  Bounded (100 records)    |
|  for inference         |   |  Canonicalized JSON       |
+------------------------+   +---------------------------+
                                          |
                                          v
                            +---------------------------+
                            |  RECOVERY DETECTION       |
                            |                           |
                            |  DISCONNECTED/DEGRADED    |
                            |       -> CONNECTED        |
                            |  = recovery event         |
                            +---------------------------+
                                          |
                                          v
                            +---------------------------+
                            |  SYNCHRONIZATION MANIFEST |
                            |  (software only)          |
                            |                           |
                            |  event_id list            |
                            |  payload digests          |
                            |  sequence numbers         |
                            |  validation check         |
                            |                           |
                            |  NO network transmission  |
                            |  NO cloud endpoint        |
                            +---------------------------+
                                          |
                                          v
                            +---------------------------+
                            |  AUDITABLE EVIDENCE       |
                            |                           |
                            |  data/evidence/           |
                            |  v4_demo_scenario.json    |
                            +---------------------------+
```

---

## Deployment Architecture

```
+------------------------------------------------------------------+
|  DEPLOYMENT LAYER                                                |
+------------------------------------------------------------------+

PyTorch checkpoint (CPU reference)
    |
    |  VERIFIED
    v
ONNX Runtime (CPUExecutionProvider)
    |  - Static ONNX: [1, 12, 17] -> [1]
    |  - Dynamic ONNX: [batch, 12, 17] -> [batch]
    |  - Numerical equivalence: max error 5.96e-08 (threshold 1e-5)
    |  - Batch-1 speedup vs PyTorch: ~5.88x (CPU-to-CPU measurement)
    |
    |  VERIFIED
    v
[PLANNED] Qualcomm QNN Conversion
    |
    |  NOT VERIFIED — requires QNN SDK and Snapdragon hardware
    v
[PLANNED] Snapdragon NPU Execution
    |
    |  NOT VERIFIED — requires actual Snapdragon device
    v
[PLANNED] Edge Deployment on Snapdragon Platform
```

---

## Component Map

| Component | File | Classification | Status |
|---|---|---|---|
| Temporal predictor architecture | src/ai/temporal_predictor.py | new EdgeResilience | VALIDATED |
| V4 inference engine | src/ai/v4_inference.py | new EdgeResilience | VALIDATED |
| V4 risk interpretation | src/resilience/v4_risk.py | new EdgeResilience | VALIDATED |
| V4 edge runtime | src/resilience/v4_runtime.py | new EdgeResilience | VALIDATED |
| Connectivity policy | src/resilience/connectivity.py | new EdgeResilience | VALIDATED |
| Evidence buffer | src/resilience/evidence_buffer.py | new EdgeResilience | VALIDATED |
| Synchronization manifest | src/resilience/synchronization.py | new EdgeResilience | VALIDATED |
| Dashboard server | src/dashboard/server.py | new EdgeResilience | VALIDATED |
| Snapdragon deployment module | src/snapdragon/deployment.py | new EdgeResilience | CPU+ONNX VALIDATED |
| Vehicle CAN modules | src/vehicle/*_inherited.py | inherited/reference | NOT used in V4 |

---

## AI vs Deterministic Separation

```
AI INFERENCE LAYER (probabilistic)
    EdgeResilienceTemporalPredictor
    -> predicted_future_degradation (float, 0-1)

        |
        | boundary: AI output -> deterministic policy input
        v

DETERMINISTIC POLICY LAYER
    V4_DEGRADATION_DEMO_POLICY_V1
    -> risk_level (categorical)
    -> evidence_required (boolean)
    -> connectivity_decision (categorical)
    -> synchronization_allowed (boolean)

        |
        | boundary: policy output -> resilience state
        v

RESILIENCE STATE LAYER
    -> local_inference_allowed
    -> local_buffering_required
    -> recovery_detected
    -> synchronization_ready
    -> evidence_count
```

AI components do not directly command vehicle actuation.
All safety-relevant state transitions are deterministic.

---

## Three-Cycle Demo Scenario

```
cycle-001: CONNECTED
    prediction: ~0.0339  risk: LOW
    local inference: YES  buffering: NO
    recovery: NO  sync: NO

cycle-002: DISCONNECTED (connectivity lost)
    prediction: ~0.0031  risk: NORMAL
    local inference: YES  buffering: YES  (evidence preserved)
    recovery: NO  sync: NO

cycle-003: CONNECTED (connectivity recovered)
    prediction: ~0.0436  risk: MEDIUM
    local inference: YES  buffering: NO
    recovery: YES  sync: READY
```

---

## Safety Boundary

This is a software simulation / virtual laboratory.

- Physical vehicle testing: NO
- Production vehicle connection: NO
- External CAN transmission: NO
- Direct vehicle actuation: NO
- Steering / braking / throttle control: NO
- Real emergency dispatch: NO
- Real public-safety integration: NO

---

## Future Architecture (V2X — not yet implemented)

The next major expansion is V2X Agentic AI Cooperative Cyber Resilience.
When EdgeResilience predicts a cyber threat, Vehicle A can broadcast a
structured cooperative alert to nearby V2X vehicles. Neighbors independently
validate, form geographic threat clusters, and optionally escalate to a
mock city safety interface (simulation only).

This is FUTURE work. It does not affect the current validated V4 baseline.
See docs/FINAL_TECHNICAL_BASELINE.md section 32 for the roadmap.
