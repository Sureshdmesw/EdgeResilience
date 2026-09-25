# Phase 11A Evidence Manifest

| Evidence | Artifact | Status |
|---|---|---|
| AI Hub compile | `job_j5wlly94p_optimized_onnx_mq26v56jn.onnx.zip` | PASS |
| Optimized ONNX | `extracted\job_j5wlly94p_optimized_onnx\model.onnx` | PASS |
| AI Hub profile | `profile_jg9zzvxmp.json` | PASS |
| Profile trace | `jg9zzvxmp_1_0_profile_trace.json` | PASS |
| QHAS summary | `jg9zzvxmp_1_0_qhas_summary.json` | PASS |
| Runtime log | `jg9zzvxmp_runtime.log` | PASS |
| Snapdragon zero inference | `inference_j56886mvg.h5` | PASS |
| Snapdragon ones inference | `dataset-d9em61ko2.h5` | PASS |
| Pre-sigmoid debug | `debug_pre_sigmoid.onnx` | ANALYSIS |
| Output trace | `trace_outputs.py` | ANALYSIS |
| CPU reference equivalence | Four optimized-ONNX test inputs | PASS |
| CPU-to-Snapdragon equivalence | Actual Snapdragon tensors | NOT ESTABLISHED |
| HP physical deployment | Specific HP Snapdragon PC | NOT MEASURED |
| Power | Project-specific measurement | NOT MEASURED |
| Thermal | Project-specific measurement | NOT MEASURED |
