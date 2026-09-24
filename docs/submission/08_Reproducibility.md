# EdgeResilience — 08: Reproducibility

## Minimum Requirements

```
Python 3.9+
pip install torch onnxruntime numpy scikit-learn joblib
```

Tested on: Python 3.11.9, PyTorch 2.14.0+cpu, ONNX Runtime 1.30.0

---

## Five Commands to Reproduce Everything

```bash
# 1. Validate all core modules compile
python -m py_compile src\ai\v4_inference.py
python -m py_compile src\resilience\v4_runtime.py
python -m py_compile src\dashboard\server.py
python -m py_compile demo\run_demo.py

# 2. Run the V4 demo
python demo\run_demo.py

# 3. Generate V4 evidence artifact
python scripts\generate_v4_demo_evidence.py

# 4. Validate ONNX equivalence
python scripts\validate_v4_dynamic_onnx_equivalence.py

# 5. Start the dashboard
python src\dashboard\server.py
# Open: http://127.0.0.1:8765
```

---

## Protected Artifact Checksums

Verify these have not changed before any operation:

```python
import hashlib
from pathlib import Path

expected = {
    'models/edgeresilience/temporal_predictor_v4.pt':
        'b551ad9f02b56668ef3f8f7873133748275307f1934ec7fd77da14e7325d26b9',
    'data/processed/temporal/edgeresilience_temporal_dataset_v4.jsonl':
        '02a82f0f5ee78dc4e3be28b81b53b6eb4eb884600a4734f3eb3aaa279cb3a911',
    'models/edgeresilience/temporal_predictor_v4_dynamic.onnx':
        'acb43a20c9fa64577c56bdfe3aa3c2ea96b6691420c0a7994dc5fd9f230c0e5d',
}

for path, sha in expected.items():
    actual = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    print('OK' if actual == sha else 'MISMATCH', path)
```

---

## Expected Demo Output (Deterministic)

Given the fixed checkpoint and dataset records 0/1/2:

| Cycle | predicted_future_degradation | risk_level |
|---|---|---|
| cycle-001 | 0.033857 | LOW |
| cycle-002 | 0.003141 | NORMAL |
| cycle-003 | 0.043561 | MEDIUM |

These values are deterministic. They will be identical on any
machine running the same checkpoint and input records.

---

## Key Artifact Paths

| Artifact | Path |
|---|---|
| V4 checkpoint | models/edgeresilience/temporal_predictor_v4.pt |
| V4 dynamic ONNX | models/edgeresilience/temporal_predictor_v4_dynamic.onnx |
| V4 dataset | data/processed/temporal/edgeresilience_temporal_dataset_v4.jsonl |
| V4 demo evidence | data/evidence/v4_demo_scenario.json |
| Training report | models/edgeresilience/temporal_predictor_v4_report.json |
| Ablation report | experiments/v4_neural_ablation_report.json |
| ONNX equivalence | experiments/v4_dynamic_onnx_equivalence_report.json |
| CPU benchmark | experiments/cpu_reference_benchmark_v4.json |
| ONNX benchmark | experiments/v4_pytorch_vs_onnx_cpu_benchmark.json |
| Deployment manifest | experiments/snapdragon_deployment_manifest_v4.json |

---

## Full Documentation Index

| Document | Purpose |
|---|---|
| README.md | Project overview |
| QUICKSTART.md | Fastest path to run demo |
| docs/FINAL_TECHNICAL_BASELINE.md | Complete technical reference |
| docs/architecture/ARCHITECTURE.md | System architecture diagrams |
| docs/REPRODUCIBILITY.md | Full environment details |
| docs/EVIDENCE_INDEX.md | All evidence artifacts indexed |
| docs/SNAPDRAGON_DEPLOYMENT.md | Deployment status and path |
| docs/COMPETITION_CLAIMS.md | Allowed/disallowed wording |
| docs/SAFETY_BOUNDARY.md | Safety boundary statement |
| docs/MODEL_CARD_V4.md | Model card |
| docs/DATA_CARD_V4.md | Dataset card |
| docs/EXPERIMENT_SUMMARY.md | All experiment results |
| docs/provenance/PROVENANCE_REGISTER.md | Artifact classification |
