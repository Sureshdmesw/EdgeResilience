# EdgeResilience — 06: Working Demo

## What the Demo Shows

The EdgeResilience demo is a reproducible, evidence-backed
three-cycle scenario using the actual V4 temporal predictor
checkpoint. It demonstrates the complete pipeline end-to-end.

---

## Run the Demo

```
python demo\run_demo.py
```

Expected output:

```
========================================================================
EDGERESILIENCE V4 SOFTWARE DEMONSTRATION
Model: EdgeResilience_V4_TemporalPredictor
Target: future_degradation
========================================================================

[cycle-001] Predictive warning / connected
  Future degradation:  0.033857
  Risk level:          LOW
  Policy:              V4_DEGRADATION_DEMO_POLICY_V1
  Connectivity:        CONNECTED
  Local inference:     True
  Local buffering:     False
  Evidence records:    0
  Recovery detected:   False
  Sync ready:          False

[cycle-002] Connectivity loss / local resilience
  Future degradation:  0.003141
  Risk level:          NORMAL
  Policy:              V4_DEGRADATION_DEMO_POLICY_V1
  Connectivity:        DISCONNECTED
  Local inference:     True
  Local buffering:     True
  Evidence records:    1
  Recovery detected:   False
  Sync ready:          False

[cycle-003] Connectivity recovery / synchronization
  Future degradation:  0.043561
  Risk level:          MEDIUM
  Policy:              V4_DEGRADATION_DEMO_POLICY_V1
  Connectivity:        CONNECTED
  Local inference:     True
  Local buffering:     False
  Evidence records:    2
  Recovery detected:   True
  Sync ready:          True

========================================================================
DEMO SCENARIO: PASS
========================================================================
```

---

## What Each Cycle Demonstrates

### cycle-001: Predictive Warning / Connected

- V4 model runs inference on 17 features × 12 steps
- Predicted degradation: 0.0339 → risk level LOW
- Vehicle is CONNECTED — normal operation
- Local inference active, no buffering needed

**Key point:** The model is predicting *future* degradation,
not reacting to a current anomaly. This is the predictive edge.

### cycle-002: Connectivity Loss / Local Resilience

- Connectivity lost (heartbeat failure, 85% packet loss)
- V4 model **continues running locally** — no cloud dependency
- Predicted degradation: 0.0031 → risk NORMAL
- Evidence record buffered locally with SHA-256 digest
- Synchronization blocked until connectivity recovers

**Key point:** Local inference never stops. The edge AI pipeline
is fully autonomous during connectivity loss.

### cycle-003: Connectivity Recovery / Synchronization

- Connectivity restored
- Recovery transition detected: DISCONNECTED → CONNECTED
- Predicted degradation: 0.0436 → risk MEDIUM (evidence required)
- Synchronization manifest prepared from buffered records
- Evidence chain is complete and verifiable

**Key point:** The system detects recovery, prepares the
synchronization manifest, and the evidence chain is intact.

---

## Demo Configuration

| Property | Value |
|---|---|
| Model | EdgeResilience_V4_TemporalPredictor |
| Checkpoint | models/edgeresilience/temporal_predictor_v4.pt |
| Dataset records used | records[0], records[1], records[2] |
| Policy | V4_DEGRADATION_DEMO_POLICY_V1 |
| Evidence artifact | data/evidence/v4_demo_scenario.json |

Source: experiments/demo_config_record.json

---

## Demo Assertions (Verified)

The demo runner verifies these assertions programmatically:

```python
assert final["recovery_detected"] is True
assert final["synchronization_ready"] is True
assert final["local_buffering_required"] is False
```

If any assertion fails, the demo exits with an error.
The demo has passed every run since the V4 baseline was validated.

---

## Safety Boundary

```
Physical vehicle test:       NO
External CAN transmission:   NO
Direct actuation:            NO
Production vehicle:          NO
Snapdragon X Elite:          VERIFIED — COMPONENT / WORKLOAD
Qualcomm QNN / HTP:          VERIFIED — COMPONENT / WORKLOAD
Full CPU ↔ Snapdragon numerical equivalence: NOT VERIFIED
```
