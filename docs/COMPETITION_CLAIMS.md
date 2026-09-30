# EdgeResilience — Competition Claims Audit

This document defines the allowed and disallowed wording for every major
claim in the EdgeResilience competition submission. Use this as a checklist
before finalizing any presentation, README, or demo material.

---

## V4 Prediction

| Field | Value |
|---|---|
| Claim | The V4 model predicts future resilience degradation |
| Evidence | models/edgeresilience/temporal_predictor_v4_report.json |
| Status | VERIFIED |
| Allowed | "The V4 temporal predictor predicts future_degradation from 17 cyber features over 12 observation steps" |
| Allowed | "Test MAE approximately 0.0051, RMSE approximately 0.0066" |
| Disallowed | "Predicts vehicle crashes" |
| Disallowed | "Certified safety prediction" |
| Disallowed | "Physical vehicle validated" |

---

## Temporal Modeling

| Field | Value |
|---|---|
| Claim | Temporal trajectory improves prediction over single-step input |
| Evidence | experiments/v4_neural_ablation_report.json |
| Status | VERIFIED |
| Allowed | "Full 12-step sequence outperforms final-step-only input (MAE 0.0052 vs 0.0067)" |
| Allowed | "Temporal attention pooling weights each observation step by relevance" |
| Disallowed | "Best possible temporal model" |
| Disallowed | "Outperforms all baselines" |

---

## Synthetic Dataset

| Field | Value |
|---|---|
| Claim | V4 was trained on EdgeResilience synthetic temporal scenario data |
| Evidence | data/processed/temporal/edgeresilience_temporal_dataset_v4_manifest.json |
| Status | VERIFIED |
| Allowed | "5,000 synthetic EdgeResilience temporal scenarios, 17 features, 12 steps" |
| Allowed | "Synthetic cyber-physical scenario features derived from domain knowledge" |
| Disallowed | "Trained on real vehicle telemetry" |
| Disallowed | "Trained directly on raw HCRL measurements" |
| Disallowed | "Real-world crash data" |

---

## ONNX Deployment

| Field | Value |
|---|---|
| Claim | V4 model is exported to ONNX and numerically equivalent to PyTorch |
| Evidence | experiments/v4_dynamic_onnx_equivalence_report.json |
| Status | VERIFIED |
| Allowed | "Dynamic ONNX export validated across batch sizes 1, 4, 16 with max error 5.96e-08" |
| Allowed | "ONNX Runtime CPUExecutionProvider verified" |
| Disallowed | "ONNX on Snapdragon verified" |
| Disallowed | "QNN execution verified" |

---

## CPU Performance

| Field | Value |
|---|---|
| Claim | ONNX Runtime is ~5.88x faster than PyTorch on the same CPU |
| Evidence | experiments/v4_pytorch_vs_onnx_cpu_benchmark.json |
| Status | VERIFIED |
| Allowed | "~5.88x mean latency improvement: ONNX Runtime vs PyTorch on Intel Core i5-1235U" |
| Allowed | "ONNX CPU mean latency: 0.267 ms (batch-1)" |
| Allowed | "CPU-to-ONNX deployment evidence" |
| Disallowed | "Snapdragon acceleration" |
| Disallowed | "NPU speedup" |
| Disallowed | "Qualcomm acceleration" |
| Disallowed | "Edge hardware speedup" |

---

## Snapdragon

| **Field** | **Value** |
| --- | --- |
| **Claim** | Snapdragon deployment has been partially verified at the component and workload level |
| **Evidence** | `docs/snapdragon/SNAPDRAGON_VALIDATION.md`; `docs/qualcomm_aihub_hardware_validation.md`; `docs/qualcomm_aihub_htp_validation.md` |
| **Status** | **PARTIALLY VERIFIED — COMPONENT / WORKLOAD LEVEL** |
| **Verified** | Snapdragon X Elite CRD hardware execution of validated V4 components and the temporal-pooling + prediction-head workload |
| **Verified components** | Encoder Block 1, Encoder Block 2, Temporal Pooling, Prediction Head, QKV structural control, Attention-block structural control |
| **Verified workload** | V4 Temporal Pooling + Prediction Head |
| **Device** | Snapdragon X Elite CRD / SC8380XP / Hexagon v73 |
| **Allowed** | "Snapdragon X Elite hardware execution verified for validated V4 components" |
| **Allowed** | "Snapdragon X Elite HTP execution verified for the temporal-pooling + prediction-head workload" |
| **Allowed** | "Snapdragon component-level validation completed" |
| **Disallowed** | "Complete V4 model runs on Snapdragon" |
| **Disallowed** | "Complete V4 Snapdragon end-to-end validation verified" |
| **Disallowed** | "Snapdragon numerical equivalence verified" |
| **Disallowed** | "Physical vehicle validation performed" |

---

## Qualcomm QNN

| **Field** | **Value** |
| --- | --- |
| **Claim** | Qualcomm QNN/HTP compilation and execution have been verified for selected V4 components and the temporal-pooling + prediction-head workload |
| **Evidence** | `docs/qualcomm_aihub_hardware_validation.md`; `docs/qualcomm_aihub_htp_validation.md`; `docs/snapdragon/SNAPDRAGON_VALIDATION.md` |
| **Status** | **VERIFIED — COMPONENT / WORKLOAD LEVEL** |
| **Runtime** | Qualcomm QNN HTP |
| **Device** | Snapdragon X Elite CRD |
| **Compile evidence** | `jp0mjdr2g` |
| **Profile evidence** | `jp3z9xmx5` |
| **Verified** | QNN HTP initialization, model loading, inference execution and HTP profiling for the validated workload |
| **Allowed** | "Qualcomm QNN/HTP execution verified for validated V4 components" |
| **Allowed** | "Qualcomm QNN/HTP profiling completed successfully for the validated workload" |
| **Disallowed** | "Complete V4 QNN/HTP execution verified" |
| **Disallowed** | "CPU-to-Snapdragon numerical equivalence verified" |

---

## NPU

| **Field** | **Value** |
| --- | --- |
| **Claim** | Qualcomm HTP/NPU execution has been verified for the full production V4 model profile |
| **Evidence** | experiments/snapdragon/profile_artifacts/v4_full_production; QAI Hub profile job jpxlwmxlp |
| **Status** | **VERIFIED - FULL PRODUCTION V4 PROFILE** |
| **Device** | Snapdragon X Elite CRD |
| **Estimated inference time** | 63 us |
| **Warm median latency** | 67 us |
| **Warm mean latency** | 68.96 us |
| **Warm P90 / P95 / P99** | 77 / 82 / 88 us |
| **Peak inference memory** | 28.5 MB |
| **NPU-executed profile entries** | 90 / 90 |
| **HTP utilization** | NOT EXPOSED BY QAI Hub PROFILE |
| **Warm single-batch throughput estimate** | ~14,501 inferences/s |
| **Allowed** | Full production V4 HTP/NPU execution was profiled successfully |
| **Allowed** | Estimated full-production V4 inference latency was 63 us on the Snapdragon X Elite CRD profile |
| **Allowed** | Warm single-batch profile corresponds to approximately 14,501 inferences/s at the warm mean |
| **Disallowed** | Any percentage HTP-utilization claim not directly exposed by the profile |
| **Disallowed** | CPU-to-Snapdragon numerical equivalence verified |
| **Disallowed** | 63 us is a sustained production throughput benchmark |

---

## Snapdragon Numerical Validation

| **Field** | **Value** |
| --- | --- |
| **Claim** | CPU-to-Snapdragon numerical equivalence for the complete V4 production model has not been established |
| **Status** | **FAILED** |
| **Authoritative validator** | experiments/v4_cpu_snapdragon_numerical_equivalence.json |
| **Max absolute error** | 0.0030923495 |
| **Mean absolute error** | 0.0030923495 |
| **RMSE** | 0.0030923495 |
| **Max relative error** | 38.50% |
| **Acceptance thresholds** | Max absolute 1e-4; mean absolute 1e-5 |
| **Result** | CPU-to-Snapdragon numerical equivalence does not meet the established acceptance thresholds |
| **Diagnostic finding** | First material production-path divergence was localized to LayerNorm |
| **Diagnostic status** | Investigation completed; multiple precision, reduction, and fusion hypotheses were tested without establishing numerical equivalence |
| **Reporting boundary** | Snapdragon hardware execution and HTP profiling must not be interpreted as CPU-to-Snapdragon numerical equivalence |

## Edge AI

| Field | Value |
|---|---|
| Claim | EdgeResilience is an edge AI system |
| Evidence | V4 runtime, ONNX export, local inference |
| Status | VERIFIED (CPU + ONNX) |
| Allowed | "Local edge inference — no cloud dependency for prediction" |
| Allowed | "ONNX deployment enables edge runtime" |
| Allowed | "Designed for Snapdragon-powered edge compute" |
| Disallowed | "Deployed on Snapdragon edge hardware" (unless verified) |

---

## Local Inference

| Field | Value |
|---|---|
| Claim | Inference continues locally when connectivity is lost |
| Evidence | data/evidence/v4_demo_scenario.json (cycle-002) |
| Status | VERIFIED |
| Allowed | "V4 model runs locally regardless of connectivity state" |
| Allowed | "cycle-002 demonstrates local inference during DISCONNECTED state" |
| Disallowed | "Requires cloud connectivity" |

---

## Connectivity Resilience

| Field | Value |
|---|---|
| Claim | System maintains operation during connectivity loss |
| Evidence | data/evidence/v4_demo_scenario.json |
| Status | VERIFIED |
| Allowed | "Three-cycle demo: connected -> disconnected (local buffering) -> recovery + sync" |
| Disallowed | "Tested on real vehicle network" |

---

## Evidence Preservation

| Field | Value |
|---|---|
| Claim | Evidence is buffered locally with SHA-256 integrity |
| Evidence | src/resilience/evidence_buffer.py, v4_demo_scenario.json |
| Status | VERIFIED |
| Allowed | "SHA-256 hashed, UTC-timestamped evidence records" |
| Allowed | "Bounded local buffer (100 records)" |
| Disallowed | "Transmitted to cloud during disconnection" |

---

## Recovery and Synchronization

| Field | Value |
|---|---|
| Claim | System detects connectivity recovery and prepares synchronization |
| Evidence | data/evidence/v4_demo_scenario.json (cycle-003) |
| Status | VERIFIED (software manifest only) |
| Allowed | "Recovery detected on DISCONNECTED -> CONNECTED transition" |
| Allowed | "Synchronization manifest prepared (software only — no network transmission)" |
| Disallowed | "Data transmitted to cloud" |
| Disallowed | "Real network synchronization" |

---

## Physical Vehicle

| **Field** | **Value** |
| --- | --- |
| **Claim** | No physical vehicle testing was performed |
| **Status** | **CONFIRMED � NOT PERFORMED** |
| **Current validation boundary** | Dataset, simulation, HIL/software validation, and Snapdragon hardware/component validation |
| **Future work** | Physical vehicle / ECU validation remains future work |
| **Disallowed** | Any claim implying road testing, physical vehicle testing, physical ECU actuation, or external CAN transmission |

---

## CAN Bus

| Field | Value |
|---|---|
| Claim | No external CAN transmission was performed |
| Evidence | safety_boundary.physical_vehicle = false |
| Status | CONFIRMED |
| Allowed | "Virtual CAN/HIL laboratory concept" |
| Allowed | "CAN features are synthetic scenario representations" |
| Disallowed | "Transmitted on real CAN bus" |
| Disallowed | "Connected to vehicle OBD port" |

---

## Actuation

| Field | Value |
|---|---|
| Claim | No direct vehicle actuation was performed |
| Evidence | safety_boundary.direct_actuation = false |
| Status | CONFIRMED |
| Allowed | "AI outputs are separated from deterministic safety policy" |
| Allowed | "No vehicle actuation commands" |
| Disallowed | "Controls vehicle steering/braking/throttle" |
| Disallowed | "Autonomous vehicle control" |
