# EdgeResilience — Reproducibility Guide

This document provides all information needed to reproduce the EdgeResilience
V4 competition results from the existing repository artifacts.

---

## Python Environment

| Component | Version |
|---|---|
| Python | 3.11.9 |
| PyTorch | 2.12.1+cpu |
| ONNX Runtime | 1.30.0 |
| NumPy | 2.4.6 |
| scikit-learn | 1.9.0 |
| joblib | (installed with scikit-learn) |

Install:

```
pip install torch onnxruntime numpy scikit-learn joblib
```

---

## Protected Artifact Checksums

These artifacts must not change. Verify before and after any operation.

| Artifact | SHA256 |
|---|---|
| models/edgeresilience/temporal_predictor_v4.pt | b551ad9f02b56668ef3f8f7873133748275307f1934ec7fd77da14e7325d26b9 |
| data/processed/temporal/edgeresilience_temporal_dataset_v4.jsonl | 02a82f0f5ee78dc4e3be28b81b53b6eb4eb884600a4734f3eb3aaa279cb3a911 |
| models/edgeresilience/temporal_predictor_v4_dynamic.onnx | acb43a20c9fa64577c56bdfe3aa3c2ea96b6691420c0a7994dc5fd9f230c0e5d |

Verify with:

```
python -c "
import hashlib
from pathlib import Path

artifacts = {
    'models/edgeresilience/temporal_predictor_v4.pt':
        'b551ad9f02b56668ef3f8f7873133748275307f1934ec7fd77da14e7325d26b9',
    'data/processed/temporal/edgeresilience_temporal_dataset_v4.jsonl':
        '02a82f0f5ee78dc4e3be28b81b53b6eb4eb884600a4734f3eb3aaa279cb3a911',
    'models/edgeresilience/temporal_predictor_v4_dynamic.onnx':
        'acb43a20c9fa64577c56bdfe3aa3c2ea96b6691420c0a7994dc5fd9f230c0e5d',
}

for path, expected in artifacts.items():
    actual = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    status = 'OK' if actual == expected else 'MISMATCH'
    print(f'{status}: {path}')
"
```

---

## Model Configuration

| Parameter | Value |
|---|---|
| input_features | 17 |
| sequence_length | 12 |
| d_model | 64 |
| nhead | 4 |
| num_layers | 2 |
| dim_feedforward | 128 |
| dropout | 0.1 |

Source: models/edgeresilience/temporal_predictor_v4_report.json

---

## Training Configuration

| Parameter | Value |
|---|---|
| Optimizer | AdamW |
| Learning rate | 0.001 |
| Weight decay | 0.0001 |
| Batch size | 128 |
| Max epochs | 80 |
| Best epoch | 77 |
| Random seed | 42 |
| Train samples | 3,200 |
| Validation samples | 800 |
| Test samples | 1,000 |
| Split | 80/20 train-test, then 80/20 train-validation |
| Device | CPU |

---

## Validated Test Metrics

| Metric | Value |
|---|---|
| Test MAE | 0.0051398626528680325 |
| Test RMSE | 0.0065667886115105215 |
| Mean baseline MAE | 0.020320536568760872 |
| Mean baseline RMSE | 0.02322702348925588 |
| Beats mean baseline | True |

Source: models/edgeresilience/temporal_predictor_v4_report.json

---

## Temporal Ablation Results

| Input representation | MAE | RMSE |
|---|---|---|
| Final timestep only | 0.0067 | 0.0086 |
| Final + delta + std | 0.0053 | 0.0068 |
| Full 12-step sequence | 0.0052 | 0.0066 |

Source: experiments/v4_neural_ablation_report.json

---

## ONNX Equivalence

Dynamic ONNX batch equivalence (threshold 1e-5):

| Batch | Max absolute error | Result |
|---|---|---|
| 1 | 4.38e-08 | PASS |
| 4 | 3.54e-08 | PASS |
| 16 | 5.96e-08 | PASS |

Source: experiments/v4_dynamic_onnx_equivalence_report.json

---

## CPU Benchmark Configuration

| Parameter | Value |
|---|---|
| Input shape | [1000, 12, 17] |
| Samples per run | 1,000 |
| Warmup runs | 20 |
| Benchmark runs | 100 |
| Hardware | Intel Core i5-1235U (reference CPU) |

Source: experiments/cpu_reference_benchmark_v4.json

---

## Demo Reproduction

Run the demo:

```
python demo\run_demo.py
```

The demo uses:
- Checkpoint: models/edgeresilience/temporal_predictor_v4.pt
- Dataset: data/processed/temporal/edgeresilience_temporal_dataset_v4.jsonl (records 0, 1, 2)
- Connectivity scenarios: hardcoded (see demo/run_demo.py)

Expected predictions (deterministic given fixed checkpoint and inputs):

| Cycle | predicted_future_degradation | risk_level |
|---|---|---|
| cycle-001 | 0.033857 | LOW |
| cycle-002 | 0.003141 | NORMAL |
| cycle-003 | 0.043561 | MEDIUM |

---

## Evidence Generation

```
python scripts\generate_v4_demo_evidence.py
```

Output: data/evidence/v4_demo_scenario.json

---

## Dashboard

```
python src\dashboard\server.py
```

URL: http://127.0.0.1:8765
API: http://127.0.0.1:8765/api/evidence

---

## Deployment Audit

```
python -c "
import json
from pathlib import Path
m = json.loads(Path('experiments/snapdragon_deployment_manifest_v4.json').read_text())
print('Status:', m['status'])
for b in m['backends']:
    print(f'  {b[\"name\"]}: verified={b[\"verified\"]}')
"
```

---

## Notes

- The PyTorch UserWarning about `enable_nested_tensor` is benign. It is a
  known PyTorch message when `norm_first=True` is used in TransformerEncoder.
  It does not affect model correctness or output.

- All benchmarks were performed on Windows / Intel Core i5-1235U.
  Snapdragon X Elite CRD component/workload execution and HTP profiling were subsequently validated through Qualcomm AI Hub.

- The ~5.88x ONNX speedup is a CPU-to-CPU measurement. It is NOT a
  Snapdragon or NPU result.
