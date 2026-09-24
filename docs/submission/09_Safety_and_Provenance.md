# EdgeResilience — 09: Safety and Provenance

## Safety Boundary

EdgeResilience is a **software simulation / virtual laboratory**.

| Activity | Status |
|---|---|
| Software simulation | YES — this is what the project is |
| Synthetic vehicle scenarios | YES |
| Virtual CAN/HIL concepts | YES |
| Physical vehicle testing | NO |
| Production vehicle connection | NO |
| External CAN bus transmission | NO |
| Direct vehicle actuation | NO |
| Steering / braking / throttle control | NO |
| Real emergency dispatch | NO |
| Real public-safety integration | NO |

AI outputs are separated from deterministic safety policy.
The V4 model informs risk level. It does not command actuation.

The risk interpretation policy (V4_DEGRADATION_DEMO_POLICY_V1) is:
- A deterministic demonstration policy
- NOT a certified vehicle safety policy
- NOT learned thresholds
- NOT Snapdragon hardware limits
- NOT physical vehicle safety limits

---

## Snapdragon Claim Boundary

| Claim | Status |
|---|---|
| Designed for Snapdragon deployment | YES — architecture and ONNX export |
| CPU reference inference | VERIFIED |
| ONNX Runtime CPU inference | VERIFIED |
| ONNX numerical equivalence | VERIFIED |
| Qualcomm QNN / HTP execution | VERIFIED — COMPONENT / WORKLOAD LEVEL |
| Snapdragon X Elite execution | VERIFIED — COMPONENT / WORKLOAD LEVEL |
| HTP/NPU profiling | VERIFIED — VALIDATED WORKLOAD |
| Full CPU ↔ Snapdragon numerical equivalence | NOT VERIFIED |
| Full V4 Snapdragon latency | NOT CLAIMED |
| Snapdragon power | NOT MEASURED |
| Snapdragon thermal | NOT MEASURED |

The ~5.88× ONNX speedup is a CPU-to-CPU measurement on an Intel
Core i5-1235U. It is NOT a Snapdragon result.

The Snapdragon HTP profile reports approximately 36 µs estimated
inference time and 97.22% HTP utilization for the profiled workload.
These figures must not be interpreted as full V4 vehicle-system latency
or CPU-to-Snapdragon numerical equivalence.

---

## Provenance Classification

| Artifact | Classification |
|---|---|
| V4 temporal predictor | VALIDATED — new EdgeResilience artifact |
| V4 dataset | VALIDATED — new EdgeResilience synthetic artifact |
| V4 ONNX exports | VALIDATED — new EdgeResilience artifact |
| V4 inference engine | VALIDATED — new EdgeResilience artifact |
| V4 risk policy | VALIDATED — new EdgeResilience artifact |
| V4 runtime | VALIDATED — new EdgeResilience artifact |
| Connectivity module | VALIDATED — new EdgeResilience artifact |
| Evidence buffer | VALIDATED — new EdgeResilience artifact |
| Synchronization module | VALIDATED — new EdgeResilience artifact |
| Dashboard | VALIDATED — new EdgeResilience artifact |
| Vehicle CAN modules | INHERITED/REFERENCE — not used in V4 pipeline |
| HCRL data | INHERITED/REFERENCE — not used as V4 model input |
| Previous CRSS Transformer | INHERITED/REFERENCE — frozen, immutable, not used |
| Snapdragon X Elite | VERIFIED — COMPONENT / WORKLOAD LEVEL |
| Qualcomm QNN / HTP | VERIFIED — COMPONENT / WORKLOAD LEVEL |
| Full CPU ↔ Snapdragon numerical equivalence | NOT VERIFIED |
| Physical vehicle validation | NOT PERFORMED |

---

## Dataset Provenance

The V4 dataset is a **new EdgeResilience synthetic artifact**.

- 5,000 records, 17 features, 12 steps
- Generated using synthetic EdgeResilience temporal scenario logic
- Latent regimes used during generation — NOT exposed as model features
- Raw HCRL measurements are NOT the direct model input
- Cyber feature values are synthetic scenario features, not raw measurements
- SHA256: 02a82f0f5ee78dc4e3be28b81b53b6eb4eb884600a4734f3eb3aaa279cb3a911

---

## Project Separation

The previous project (Predictive Cyber-Physical Resilience) is
retained under `inherited/Predictive-Cyber-Physical-Resilience/`
as reference material only.

EdgeResilience has its own:
- source code, models, datasets, evidence, documentation, Git history

The inherited frozen CRSS Transformer checkpoint is immutable and
was NOT used in the EdgeResilience V4 pipeline.
