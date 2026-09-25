# Phase 11A - Snapdragon X Elite Validation

## Status

Qualcomm AI Hub compilation, Snapdragon X Elite profiling, NPU/HTP execution,
and real Snapdragon inference have been completed.

## Platform

- Device: Snapdragon X Elite CRD
- OS target: Windows
- Framework: ONNX
- Backend: Qualcomm QNN
- Accelerator: Snapdragon NPU / HTP
- AI Hub optimized model: `mq26v56jn`
- Compile job: `j5wlly94p`
- Profile job: `jg9zzvxmp`
- Zero-input inference job: `j56886mvg`
- Ones-input inference job: `jp4yyq2lp`

## Profiling Evidence

- Estimated inference time: 6876 us
- Estimated inference peak memory: 37,928,960 bytes
- First-load time: 5,809,581 us
- Warm-load time: 599,008 us
- Inference execution: NPU / HTP

## Model Structure

- Input: `image`
- Input shape: `(1,3,640,640)`
- Output 0: `(1,8400,4)` float32
- Output 1: `(1,8400)` float32
- Output 2: `(1,8400)` uint8

## CPU / Snapdragon Validation

The AI Hub optimized ONNX model was first validated against the same optimized
ONNX model using ONNX Runtime on CPU. Zeros, ones, random42 and random123
inputs produced matching CPU outputs for the optimized ONNX comparison.

Actual Snapdragon inference was then executed through Qualcomm AI Hub.

### Zero input

CPU:
- Boxes max absolute difference versus Snapdragon: 39.498718
- Boxes mean absolute difference: 0.5025143
- Scores max absolute difference: 5.263090e-05
- Scores mean absolute difference: 3.4160876e-06
- Snapdragon scores: all zero
- Snapdragon classes: class 0 only

### Ones input

Snapdragon:
- Boxes range: -66.62501 to 663.00006
- Scores range: 0 to 0.01855469
- Non-zero scores: 21 / 8400
- Classes observed: 0, 5, 6, 68
- Outputs finite: yes

## Interpretation

The Snapdragon execution path is functional and produces valid finite tensors.
However, exact CPU-to-Snapdragon numerical equivalence has not been established.

The observed divergence is input-dependent. The zero-input case produces
very small CPU sigmoid scores while the Snapdragon result is zero. The
pre-sigmoid CPU tensor was measured in the approximate range -18.0 to -9.85.

The current evidence therefore supports the following claim:

> Qualcomm AI Hub successfully compiled, profiled and executed the YOLOv11
> workload on Snapdragon X Elite NPU/HTP, while exact numerical equivalence
> with the CPU reference remains an open validation item.

No claim of exact CPU-to-Snapdragon numerical equivalence is made.

## HP Deployment Boundary

The current hardware evidence is from the Snapdragon X Elite CRD through
Qualcomm AI Hub. It is representative Snapdragon-targeted validation.

Physical measurement on a specific HP Snapdragon-powered PC has not been
performed and is therefore not claimed.

## Power / Thermal Boundary

Project-specific power and thermal measurements have not yet been captured.
Inference latency and memory measurements from Qualcomm AI Hub are available.

## Final Evidence Position

PASS:
- Qualcomm AI Hub compilation
- Snapdragon X Elite targeting
- QNN backend
- NPU/HTP execution
- Snapdragon profiling
- Actual Snapdragon inference
- Finite output tensors

NOT YET ESTABLISHED:
- Exact CPU-to-Snapdragon numerical equivalence
- Physical HP Snapdragon PC measurement
- Project-specific power measurement
- Project-specific thermal measurement
