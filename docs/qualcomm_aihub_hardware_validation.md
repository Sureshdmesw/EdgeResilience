# Qualcomm AI Hub Hardware Validation

## 1. Validation Target

- Model: EdgeResilience V4 Temporal Pooling + Prediction Head
- Device: Snapdragon X Elite CRD
- SoC: SC8380XP
- Hexagon architecture: v73
- Runtime: Qualcomm QNN HTP
- Precision: FP16
- HTP performance mode: burst
- QNN SDK: 2.45.0
- Profile Job: jp3z9xmx5
- Compile Job: jp0mjdr2g

## 2. Compile Validation

The cleaned ONNX model was successfully compiled for the Qualcomm target.

Input shape:

- add_3: (1, 12, 64), float32

Target model:

- mq9y70pl
- job_jp0mjdr2g_optimized_onnx

## 3. Inference Validation

The Qualcomm AI Hub profile successfully executed 100 inference iterations.

Primary measured inference result:

- Estimated inference time: 36 us
- Equivalent latency: 0.036 ms
- Inference peak memory: approximately 27.83 MiB
- NPU-executed layers: 29

## 4. QHAS Hardware Profile

The QHAS profile reported:

- HTP utilization: 97.22%
- HTP idle: 2.78%
- QHAS HTP time: 251 us
- Graph execution time: 40 us
- Estimated throughput: 3,984.06 inferences/s
- Timeline: 52,289 cycles
- Unique QNN operators: 14
- QNN nodes: 20
- Unique HTP operators: 14
- HTP nodes: 68

Memory traffic:

- DRAM read: 73,728 bytes
- DRAM write: 2,048 bytes
- Total DRAM traffic: 75,776 bytes
- Peak VTCM allocation: 114,688 bytes
- VTCM read: 251,904 bytes
- VTCM write: 202,752 bytes
- Total VTCM traffic: 454,656 bytes

## 5. Dominant QNN Operations

| Rank | Operation | Cycles | Active Cycles |
|------|-----------|-------:|--------------:|
| 1 | LayerNorm | 24,108 | 37.75% |
| 2 | Softmax | 9,530 | 14.92% |
| 3 | Transpose | 6,232 | 9.76% |
| 4 | Relu | 4,710 | 7.37% |
| 5 | Output | 4,223 | 6.61% |
| 6 | ReduceSum | 3,889 | 6.09% |
| 7 | Input | 3,028 | 4.74% |
| 8 | ElementWiseAdd | 1,838 | 2.88% |
| 9 | ElementWiseMultiply | 1,751 | 2.74% |
| 10 | FullyConnected | 1,746 | 2.73% |

## 6. Runtime Configuration

The profiling runtime used:

- QNN HTP Execution Provider
- HTP burst performance mode
- HTP graph finalization optimization mode 3
- FP16 precision enabled
- Normal context priority
- ONNX Runtime 1.27.1
- Profiling level: optrace

## 7. Runtime Note

The runtime reported that QNN context creation with file mapping was unsupported and automatically retried with the feature disabled. The model subsequently loaded and executed successfully.

This warning did not prevent successful inference.

## 8. Engineering Interpretation

The Qualcomm AI Hub validation provides hardware-level evidence that the EdgeResilience V4 temporal pooling and prediction-head workload executes successfully on Snapdragon X Elite HTP hardware.

The QHAS profile additionally provides evidence of high HTP utilization and identifies the dominant operator-level contributors to execution cost.

The profiling data therefore supports evaluation of the model as an edge inference component within the Predictive Cyber-Physical Resilience architecture.

## 9. Validation Status

QUALCOMM AI HUB COMPILE: PASSED

QUALCOMM HTP PROFILE: PASSED

QUALCOMM HTP INFERENCE: PASSED

QUALCOMM HARDWARE EVIDENCE PACKAGE: COMPLETE
