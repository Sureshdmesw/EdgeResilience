# EdgeResilience V4 — Data Card

---

## Dataset Details

| Property | Value |
|---|---|
| Dataset name | EdgeResilience V4 Temporal Synthetic Benchmark |
| Path | data/processed/temporal/edgeresilience_temporal_dataset_v4.jsonl |
| Manifest | data/processed/temporal/edgeresilience_temporal_dataset_v4_manifest.json |
| Records | 5,000 |
| Observation steps | 12 |
| Features per step | 17 |
| Target | future_degradation |
| Random seed | 42 |
| SHA256 | 02a82f0f5ee78dc4e3be28b81b53b6eb4eb884600a4734f3eb3aaa279cb3a911 |
| Classification | New EdgeResilience synthetic artifact |

---

## Features

The 17 features per observation step:

| # | Feature name | Notes |
|---|---|---|
| 1 | cyber_message_rate | Synthetic scenario feature |
| 2 | cyber_unique_can_id_count | Synthetic scenario feature |
| 3 | cyber_can_id_entropy | Synthetic scenario feature |
| 4 | cyber_mean_interarrival_ms | Synthetic scenario feature |
| 5 | cyber_std_interarrival_ms | Synthetic scenario feature |
| 6 | cyber_max_interarrival_ms | Synthetic scenario feature |
| 7 | cyber_interarrival_cv | Synthetic scenario feature |
| 8 | cyber_payload_change_rate | Synthetic scenario feature |
| 9 | cyber_mean_hamming_distance | Synthetic scenario feature |
| 10 | cyber_dominant_can_id_fraction | Synthetic scenario feature |
| 11 | latency_norm | Normalized connectivity latency |
| 12 | packet_loss_norm | Normalized packet loss rate |
| 13 | acceleration_norm | Normalized vehicle acceleration |
| 14 | steering_norm | Normalized steering signal |
| 15 | brake_pressure | Brake pressure signal |
| 16 | integrity | System integrity score |
| 17 | sensor_plausibility | Sensor plausibility score |

---

## Target

| Property | Value |
|---|---|
| Target name | future_degradation |
| Definition | current_resilience minus separately generated future_resilience |
| Range | Continuous, approximately [0, 1] |
| Future horizon | 6 steps |

---

## Generation Method

| Property | Value |
|---|---|
| Method | Synthetic EdgeResilience temporal scenario generation |
| Latent regimes | Used during generation — NOT exposed as model features |
| Hidden temporal memory | Used during generation — NOT exposed as model features |
| Raw HCRL records used | NO |
| Cyber values are raw HCRL measurements | NO |
| Cyber feature contract | Feature names derived from HCRL domain knowledge; values are synthetic |

The dataset uses synthetic cyber-physical scenario features. The feature
names are informed by HCRL domain knowledge, but the values are generated
synthetically. Raw HCRL measurements are NOT the direct model input.

---

## Provenance

| Property | Value |
|---|---|
| Source | This project — generated from scratch |
| Physical vehicle test | NO |
| External CAN transmission | NO |
| Direct actuation | NO |
| Production vehicle connection | NO |
| Snapdragon hardware | NOT VERIFIED |

---

## Intended Use

- Training and evaluating the EdgeResilience V4 temporal predictor
- Benchmarking temporal vs non-temporal input representations
- Competition demonstration of edge AI for connected vehicle safety

---

## Non-Intended Use

- Representing raw vehicle telemetry
- Claiming real-world vehicle validation
- Training production automotive safety systems without additional validation
- Merging with HCRL raw telemetry without explicit provenance documentation

---

## Limitations

1. Synthetic data — not validated against real vehicle telemetry
2. 5,000 records — limited diversity compared to production datasets
3. Latent regimes used during generation are not recoverable from features
4. Feature values are scenario-generated, not measured from real CAN traffic
5. Target is a synthetic resilience degradation metric, not a physical measurement

---

## Relationship to HCRL

HCRL (real cyber telemetry) is inherited/reference material from the previous
project. It was used to inform the cyber feature names and domain knowledge.

HCRL raw telemetry was NOT directly used as V4 model input.
HCRL measurements were NOT merged into this dataset.
Previous HCRL evidence is previous-project evidence.
