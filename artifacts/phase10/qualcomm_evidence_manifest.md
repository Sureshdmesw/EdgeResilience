# Phase 10 Qualcomm Evidence Manifest

## Qualcomm Compile
Compile Job: jp0mjdr2g
Target Model: mq9y70pl
Target Device: Snapdragon X Elite CRD
SoC: SC8380XP
Hexagon: v73

## Qualcomm Profile
Profile Job: jp3z9xmx5

## Model
Model: EdgeResilience V4 Temporal Pooling + Prediction Head
Input: add_3
Input Shape: (1, 12, 64)
Input Type: float32
Output: future_resilience_degradation

## Primary Profile
Estimated Inference Time: 36 us
Inference Peak Memory: approximately 27.83 MiB
NPU-Executed Layers: 29

## QHAS
HTP Utilization: 97.22%
HTP Idle: 2.78%
QHAS HTP Time: 251 us
Graph Execution Time: 40 us
Estimated Throughput: 3984.06 inferences/s

## Runtime
QNN SDK: 2.45.0
ONNX Runtime: 1.27.1
Precision: FP16
HTP Performance Mode: burst
Graph Finalization Optimization: 3
Profiling Level: optrace

## Phase 10 Objective
Connect the Qualcomm-validated V4 model to the EdgeResilience inference pipeline and verify:
1. Input compatibility
2. Reference inference correctness
3. Qualcomm inference compatibility
4. Numerical prediction consistency
5. Decision consistency
6. System-level timing
