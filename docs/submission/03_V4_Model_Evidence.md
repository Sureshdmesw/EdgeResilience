# EdgeResilience — 03: V4 Model Evidence

All numbers in this document come directly from existing validated
evidence artifacts. Nothing has been estimated or fabricated.

---

## Training Evidence

**Source:** models/edgeresilience/temporal_predictor_v4_report.json

| Metric | Value |
|---|---|
| Test MAE | 0.0051398626528680325 |
| Test RMSE | 0.0065667886115105215 |
| Mean baseline MAE | 0.020320536568760872 |
| Mean baseline RMSE | 0.023227023489255880 |
| Beats mean baseline | TRUE |
| Best epoch | 77 |
| Best validation loss | 4.378005542093888e-05 |
| Train samples | 3,200 |
| Validation samples | 800 |
| Test samples | 1,000 |
| Random seed | 42 |

---

## Temporal Ablation Evidence

**Source:** experiments/v4_neural_ablation_report.json

| Input representation | MAE | RMSE | vs final-step |
|---|---|---|---|
| final_timestep | 0.0067 | 0.0086 | baseline |
| final_plus_delta_plus_std | 0.0053 | 0.0068 | −21% MAE |
| full_12_step_sequence | 0.0052 | 0.0066 | −22% MAE |

Status: PASS

---

## Three-Cycle Demo Evidence

**Source:** data/evidence/v4_demo_scenario.json

| Cycle | Connectivity | Degradation | Risk | Buffering | Recovery | Sync |
|---|---|---|---|---|---|---|
| cycle-001 | CONNECTED | 0.033857 | LOW | No | No | No |
| cycle-002 | DISCONNECTED | 0.003141 | NORMAL | Yes | No | No |
| cycle-003 | CONNECTED | 0.043561 | MEDIUM | No | Yes | Yes |

Model: EdgeResilience_V4_TemporalPredictor
Policy: V4_DEGRADATION_DEMO_POLICY_V1
Target: future_degradation

Assertions verified:
- cycle-002: local_buffering_required = True
- cycle-003: recovery_detected = True
- cycle-003: synchronization_ready = True
- cycle-003: local_buffering_required = False

---

## Checkpoint Integrity

| Artifact | SHA256 |
|---|---|
| temporal_predictor_v4.pt | b551ad9f02b56668ef3f8f7873133748275307f1934ec7fd77da14e7325d26b9 |
| edgeresilience_temporal_dataset_v4.jsonl | 02a82f0f5ee78dc4e3be28b81b53b6eb4eb884600a4734f3eb3aaa279cb3a911 |

---

## Safety and Provenance Flags

| Flag | Value |
|---|---|
| physical_vehicle_test | FALSE |
| external_can_transmission | FALSE |
| direct_actuation | FALSE |
| production_vehicle_connection | FALSE |
| snapdragon_hardware_verified | FALSE |
| qualcomm_qnn_verified | FALSE |
| provenance | new EdgeResilience artifact |
| dataset | synthetic — NOT raw HCRL |
