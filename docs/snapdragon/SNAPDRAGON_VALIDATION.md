# EdgeResilience Snapdragon Validation

## Scope

This document records Snapdragon-targeted validation evidence for the EdgeResilience V4 temporal predictor.

Target environment:

- Device: Snapdragon X Elite CRD
- OS: Windows 11
- Chipset: Qualcomm Snapdragon X Elite / SC8380XP
- Hexagon: v73
- Runtime framework: QNN
- HTP support: available

## Full V4 Model

The V4 model was successfully compiled for the Snapdragon X Elite target.

- Compile job: `jgdd3v6zg`
- Source deployment artifact: `models/edgeresilience/snapdragon/temporal_predictor_v4_aihub.onnx`
- SHA-256: `3ADC9E8E476FB12074577C0083B5F7936A85B8093471F1A0D8349A096F185FD6`
- Compile status: VERIFIED

The complete V4 model has not yet achieved successful QNN/HTP profiling.

The full-model profile job `j5wl79zmp` failed during QNN graph finalization with error code 6000. Therefore full-model HTP execution is recorded as NOT VERIFIED.

## Exact V4 Component Validation

### Encoder Block 1

- Artifact: `v4_encoder_block1_qnn_control.onnx`
- SHA-256: `dfcc49384c374afbd5efffa21dc9cc60e9c931cbf69b07a0ab327a3393d7f214`
- Compile job: `jp4y18y8p`
- HTP profile job: `jp8ex8ekp`
- Compile: VERIFIED
- HTP: VERIFIED
- Estimated inference time: 0.045 ms
- Peak memory: 27.84765625 MiB
- NPU layers: 41
- Classification: exact V4 encoder block

### Encoder Block 2

- Artifact: `v4_encoder_block2_qnn_control.onnx`
- SHA-256: `288c40a00529807cbc5d2342fbe592d670534e5a9d3f1ef1f024e61618d226c1`
- Compile job: `jprl09qkp`
- HTP profile job: `j5qlywoep`
- Compile: VERIFIED
- HTP: VERIFIED
- Estimated inference time: 0.042 ms
- Peak memory: 27.796875 MiB
- NPU layers: 40
- Classification: exact V4 encoder block

### Temporal Pooling

The extracted component contains exact V4 nodes 74 through 86.

- Artifact: `v4_temporal_pooling_qnn_control.onnx`
- SHA-256: `567531706ca712f8ead75a8319fab0444b6e97a2a46a6f49d7d524fe7fb845e6`
- Runtime input: `add_3 [1,12,64]`
- Runtime output: `layer_norm_4 [1,64]`
- Compile job: `jgnznx8jg`
- Target model: `mm5vz7g2n`
- HTP profile job: `jp8ex6yqp`
- Compile: VERIFIED
- HTP: VERIFIED
- Estimated inference time: 0.038 ms
- Load time: 493.242 ms
- Peak memory: 28.328125 MiB
- NPU layers: 24

Raw evidence:

- Profile results JSON: `experiments/snapdragon/profile_artifacts/v4_temporal_pooling/`
- Runtime log: same directory
- Profile results SHA-256: `4E12D371DFCE61E738367DAE9C0ED06129EAEBE9A0D1A1E2BD31F1BF38136F17`
- Runtime log SHA-256: `769DCEAE691E324B6A4EF840DCBEC828EB6D0E7BBD64B72CF5C1163934481883`

## Prediction Head

- Artifact: `v4_prediction_head_qnn_control.onnx`
- Compile: VERIFIED
- HTP: VERIFIED
- Compile job: `jp1nj38lg`
- HTP profile job: `jgk24dlog`
- SHA-256: `6a6e753c16130134a960e5346cb12148d8d704bbab3283d9565ea585fa6c8afe`

## Supporting Structural Controls

The following controls independently establish Snapdragon QNN/HTP compatibility for relevant graph structures:

- QKV structural control: HTP VERIFIED
- Complete attention-block structural control: HTP VERIFIED

These are supporting controls and are not presented as complete V4 model validation.

## Reporting Boundaries

The following claims are prohibited by the evidence:

1. Component latencies must not be added together and reported as full-model latency.
2. Component memory measurements must not be added together as full-model memory.
3. CPU benchmark results must not be described as Snapdragon performance.
4. Snapdragon X Elite CRD validation must not be described as HP-branded PC validation.
5. HTP component validation must not be described as complete V4 end-to-end validation.
6. Virtual CAN/HIL experiments must not be described as physical vehicle testing.
7. No direct vehicle actuation or external CAN transmission was performed.

## Competition Deployment Position

EdgeResilience is designed around an on-device AI deployment path for Snapdragon-powered Windows PCs.

Current evidence establishes:

**Validated model → ONNX deployment artifact → Snapdragon compilation → QNN/HTP component execution**

The complete V4 graph remains a deployment optimization and validation target because its full QNN/HTP graph finalization has not yet succeeded.

## Status Vocabulary

- VERIFIED: directly demonstrated by an executed test and preserved evidence.
- PREPARED: artifact or deployment path exists but the target execution has not been fully verified.
- NOT VERIFIED: attempted and unsuccessful or not yet demonstrated.
- PLANNED: future work not yet executed.
