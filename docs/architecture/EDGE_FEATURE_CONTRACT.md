# EdgeResilience Feature Contract

## Project

EdgeResilience: Snapdragon-Powered Predictive Intelligence for Connected Vehicle Safety

## Status

Stage 3B design specification.

This document defines the proposed feature contract for the new
EdgeResilience model. It is not evidence of completed model training.

## Design principle

EdgeResilience separates:

1. Vehicle/safety state
2. Cyber telemetry state
3. Connectivity/operational state

These signals are fused only after their provenance and availability
at inference time have been established.

## Vehicle feature group

The existing validated 59-feature contract is retained as the vehicle
state representation.

Feature count: 59

The inherited frozen Transformer remains reference-only and is not
modified, retrained, fine-tuned, or replaced.

## Cyber feature group

Initial proposed cyber telemetry features:

1. cyber_message_rate
2. cyber_unique_can_id_count
3. cyber_can_id_entropy
4. cyber_mean_interarrival_ms
5. cyber_std_interarrival_ms
6. cyber_min_interarrival_ms
7. cyber_max_interarrival_ms
8. cyber_interarrival_cv
9. cyber_payload_change_rate
10. cyber_mean_hamming_distance
11. cyber_dlc_change_rate
12. cyber_dominant_can_id_fraction
13. cyber_burst_score
14. cyber_timing_anomaly_score
15. cyber_payload_anomaly_score
16. cyber_id_anomaly_score
17. cyber_attack_score

These are proposed telemetry-derived features.

HCRL attack labels are supervision/evaluation information and are
not directly supplied to the final predictive model.

## Operational/context feature group

Initial proposed features:

1. network_latency_ms
2. packet_loss_rate
3. heartbeat_failure
4. rssi_dbm
5. telemetry_gap_duration_ms
6. sensor_plausibility_score
7. integrity_score

## Initial dimensionality

Vehicle state: 59
Cyber state: 17
Operational/context: 7

Initial total: 83 features per observation.

The final feature count may change after validation, leakage checks,
missingness analysis, feature importance analysis, and ablation.

## Temporal window

Initial proposed observation window:

12 consecutive observations.

This preserves compatibility with the temporal design already used
for the inherited vehicle-state representation while keeping the new
model independently defined.

## Prediction targets

Initial targets:

Y3: predictive risk approximately 3 steps/horizon ahead
Y6: predictive risk approximately 6 steps/horizon ahead

The exact target construction will be documented before training.

## Data provenance

CRSS:
Vehicle/safety context and previously integrated source.

HCRL:
Real CAN/cyber telemetry used for cyber-behavior representation.
The four previously validated HCRL attack datasets are inherited
reference data. Their previous ingestion passed 26/26 validation checks.

Virtual EV/CAN:
Controlled cyber-physical simulation/emulation for scenario generation
and integration testing.

No physical vehicle testing is implied.

## Fusion rule

HCRL and CRSS must not be treated as naturally synchronized raw
observations.

Cyber features will first be derived from HCRL telemetry.

Cyber-physical fusion will subsequently be evaluated using explicitly
constructed and documented scenarios where the temporal relationship
between vehicle state, cyber state, and connectivity state is known.

## Leakage prevention

The following must not be used as direct production features:

- future attack labels
- future risk labels
- post-event information unavailable at inference time
- manually assigned attack class names
- future connectivity state
- future sensor state

All transformations must be causal with respect to the prediction
timestamp unless explicitly documented otherwise.

## Safety boundary

The model provides predictive intelligence and decision support.

It does not:

- directly actuate a vehicle
- transmit commands onto an external CAN bus
- control a production vehicle
- replace deterministic safety controls
- constitute physical vehicle validation

## Snapdragon boundary

Snapdragon acceleration, NPU use, Qualcomm runtime use, latency,
power, thermal behavior, and hardware deployment must only be reported
after actual verification.

CPU/reference measurements are not Snapdragon measurements.

## Status

Vehicle feature contract: inherited/reference
Cyber feature contract: new EdgeResilience design
Operational feature contract: new EdgeResilience design
Fusion model: not yet trained
Snapdragon deployment: not yet validated
