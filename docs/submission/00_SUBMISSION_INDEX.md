# EdgeResilience — Submission Package Index

**Competition:** Qualcomm Snapdragon AI Lab Build and Present Challenge
**Project:** EdgeResilience: Snapdragon-Powered Predictive Intelligence
for Connected Vehicle Safety
**Status:** Competition ready — V4 baseline + Snapdragon component/workload validation

---

## The Submission in One Paragraph

EdgeResilience is a complete edge AI pipeline for connected vehicle
cyber-physical safety, designed for on-device deployment on
Snapdragon-powered HP PCs. It trains a compact Temporal Transformer
(71K parameters) to predict future resilience degradation from 17
cyber features over 12 observation steps, maintains local inference
during connectivity loss, buffers SHA-256 hashed evidence locally,
detects connectivity recovery, and prepares a synchronization manifest.
The V4 model achieves MAE 0.0051. The ONNX export is validated with
max numerical error 5.96e-08. ONNX Runtime delivers ~5.88× lower
latency vs PyTorch on CPU. Snapdragon X Elite execution and Qualcomm QNN/HTP execution are
verified at the validated component/workload level. Full CPU-to-Snapdragon
numerical equivalence remains unverified and is under investigation.

---

## Package Contents

| # | Document | Purpose |
|---|---|---|
| 01 | 01_Problem_and_Innovation.md | Problem statement, innovation, Snapdragon fit |
| 02 | 02_Technical_Implementation.md | Architecture, components, model spec, training |
| 03 | 03_V4_Model_Evidence.md | All validated metrics and evidence artifacts |
| 04 | 04_ONNX_Deployment.md | ONNX artifacts, equivalence, CPU benchmarks |
| 05 | 05_Snapdragon_Optimization_Path.md | Specific QNN path, design rationale, honest status |
| 06 | 06_Working_Demo.md | Demo commands, expected output, cycle explanations |
| 07 | 07_Dashboard.md | Dashboard features, API, step-through demo |
| 08 | 08_Reproducibility.md | 5 commands, checksums, artifact paths |
| 09 | 09_Safety_and_Provenance.md | Safety boundary, provenance classification |
| 10 | 10_Presentation.md | Full competition presentation by evaluation category |

---

## Quick Reference: Key Numbers

| Metric | Value | Source |
|---|---|---|
| Test MAE | 0.0051 | temporal_predictor_v4_report.json |
| Test RMSE | 0.0066 | temporal_predictor_v4_report.json |
| Temporal ablation improvement | 0.0067 → 0.0052 MAE | v4_neural_ablation_report.json |
| ONNX max numerical error | 5.96e-08 | v4_dynamic_onnx_equivalence_report.json |
| ONNX CPU speedup | ~5.88× vs PyTorch | v4_pytorch_vs_onnx_cpu_benchmark.json |
| CPU throughput | 33,800 samples/sec | cpu_reference_benchmark_v4.json |
| Model parameters | 71,170 | temporal_predictor_v4_report.json |
| Dataset records | 5,000 | dataset manifest |

---

## Quick Reference: Status

| Component | Status |
|---|---|
| V4 model | VALIDATED |
| V4 dataset | VALIDATED — synthetic |
| ONNX (static + dynamic) | VALIDATED |
| CPU reference | VERIFIED |
| ONNX Runtime CPU | VERIFIED |
| Three-cycle demo | VALIDATED |
| Dashboard | OPERATIONAL |
| Qualcomm QNN/HTP | VERIFIED — COMPONENT / WORKLOAD LEVEL |
| Snapdragon X Elite | VERIFIED — COMPONENT / WORKLOAD LEVEL |
| HTP/NPU profiling | VERIFIED — VALIDATED WORKLOAD |
| Full CPU ↔ Snapdragon numerical equivalence | NOT VERIFIED |
| Physical vehicle | NOT PERFORMED |
| External CAN | NOT PERFORMED |
| Direct actuation | NOT PERFORMED |

---

## The Defensible Submission Statement

> EdgeResilience is designed for on-device deployment on
> Snapdragon-powered HP PCs. The current validated implementation
> establishes the V4 predictive model, ONNX deployment artifact,
> local inference architecture, and reproducible software
> demonstration. Snapdragon hardware and Qualcomm QNN execution
> remain explicitly unverified until tested on the target platform.
