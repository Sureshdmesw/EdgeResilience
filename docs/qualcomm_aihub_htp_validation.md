# Qualcomm AI Hub HTP Validation

## Model
EdgeResilience V4 Temporal Pooling + Prediction Head

## Target
- Device: Snapdragon X Elite CRD
- SoC: SC8380XP
- Hexagon: v73
- Runtime: Qualcomm QNN HTP
- Precision: FP16
- Performance mode: Burst

## Validation Result
Qualcomm AI Hub validation demonstrated successful HTP execution of the
EdgeResilience V4 temporal pooling and prediction-head model on a
Snapdragon X Elite CRD (SC8380XP, Hexagon v73).

The QNN HTP runtime successfully executed 100 inference iterations with:

- Estimated inference time: 36 us (0.036 ms)
- Inference peak memory: approximately 27.83 MiB
- NPU-executed layers: 29
- HTP performance mode: burst
- FP16 precision: enabled

## Runtime Validation
- Model loading completed successfully.
- Warm-load execution completed successfully.
- 100 inference iterations completed successfully.
- QNN HTP execution provider was successfully initialized.
- HTP profiling completed successfully.

## Evidence
QAI Hub Profile Job:
jp3z9xmx5

Compile Job:
jp0mjdr2g

## Engineering Interpretation
The result demonstrates that the EdgeResilience temporal pooling and
prediction-head workload can execute successfully on Qualcomm HTP hardware
with sub-millisecond inference latency.

This provides hardware-level evidence for the edge inference component of
the Predictive Cyber-Physical Resilience architecture.

## Note
The QNN runtime reported that file-mapping context creation was unsupported
and automatically retried with the feature disabled. The model subsequently
loaded and executed successfully, so this warning did not prevent inference.

## Status
QUALCOMM HTP VALIDATION: PASSED
