# Phase 10.3 Qualcomm Snapdragon Hardware Validation

## Target

Model:
`v4_temporal_pooling_plus_head_qnn_control_clean.onnx`

Target device:
Snapdragon X Elite CRD

SoC:
SC8380XP

Hexagon:
v73

Execution backend:
QNN HTP

Precision:
FP16

Performance mode:
Burst

## Qualcomm Compile

QAI Hub Compile Job:
`jp0mjdr2g`

Target model:
`mq9y70pl`

Target input:
`add_3`

Target shape:
`[1, 12, 64]`

Target dtype:
`float32`

Compile status:
SUCCESS

## Qualcomm Profile

QAI Hub Profile Job:
`jp3z9xmx5`

Profile execution:
SUCCESS

Profile iterations:
100

Estimated inference time:
36 us

Inference peak memory:
29,179,904 bytes

NPU-executed layers:
29

## QHAS Hardware Evidence

HTP utilization:
97.2193%

HTP idle:
2.7807%

QHAS HTP time:
251 us

QHAS graph execution:
40 us

Throughput:
3984.0637 inferences/sec

QNN nodes:
20

HTP nodes:
68

Unique HTP operations:
14

## Hardware Verification

Qualcomm Snapdragon hardware execution:
PASS

Qualcomm QNN HTP execution:
PASS

Numerical equivalence:
CPU/ONNX PASS

Numerical equivalence on Snapdragon hardware:
NOT YET ESTABLISHED

## Evidence

Compile Job:
`jp0mjdr2g`

Profile Job:
`jp3z9xmx5`

Target Model:
`mq9y70pl`

Profile artifacts:
`E:\EdgeResilience\artifacts\qaihub\jp3z9xmx5`

## Status

QUALCOMM_SNAPDRAGON_HARDWARE_EXECUTION = PASS
QUALCOMM_QNN_HTP_EXECUTION = PASS
QUALCOMM_NUMERICAL_EQUIVALENCE_CPU = PASS
QUALCOMM_NUMERICAL_EQUIVALENCE_HARDWARE = PENDING

## Phase 10.4 - Snapdragon Numerical Comparison

Inference job:
- jpxl4j63p: deterministic single-input validation
- jgdddnd6g: five-input validation
- Device: Snapdragon X Elite CRD
- Target model: mq9y70pln

Five-input comparison:

| Case | CPU ONNX | Snapdragon HTP | Abs Error | Relative Error |
|---:|---:|---:|---:|---:|
| 0 | 0.01151890 | 0.01302338 | 0.00150448 | 13.0610% |
| 1 | 0.01151890 | 0.01300812 | 0.00148922 | 12.9285% |
| 2 | 0.01151890 | 0.01301575 | 0.00149685 | 12.9948% |
| 3 | 0.01044959 | 0.01247406 | 0.00202447 | 19.3737% |
| 4 | 0.05127066 | 0.04891968 | 0.00235098 | 4.5854% |

Aggregate:
- Maximum absolute error: 0.0023509823
- Mean absolute error: 0.0017732024
- RMSE: 0.0018081717
- Existing numerical equivalence threshold: 0.0000100000

Result:
- Snapdragon hardware execution: PASS
- QNN HTP execution: PASS
- CPU/ONNX numerical equivalence: PASS
- CPU ONNX vs Snapdragon numerical equivalence: FAIL

Interpretation:
The compiled Qualcomm target executes successfully on Snapdragon X Elite hardware, but its output differs materially from the CPU ONNX reference across the five deterministic validation inputs. The discrepancy is input-dependent and therefore is not adequately characterized as a constant numerical offset. Further operator-level investigation is required before hardware numerical equivalence can be established.


