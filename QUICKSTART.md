# EdgeResilience — Quickstart

Shortest reliable path to run the EdgeResilience V4 competition demo.

---

## Requirements

- Python 3.9 or later
- The following packages:

```
pip install torch onnxruntime numpy scikit-learn joblib
```

All commands are run from the project root: `E:\EdgeResilience`

---

## 1. Validate the environment

```
python -m py_compile src\ai\v4_inference.py
python -m py_compile src\resilience\v4_runtime.py
python -m py_compile src\dashboard\server.py
python -m py_compile demo\run_demo.py
```

All should complete silently (exit 0).

---

## 2. Run the V4 demo

```
python demo\run_demo.py
```

Expected output:

```
EDGERESILIENCE V4 SOFTWARE DEMONSTRATION
Model: EdgeResilience_V4_TemporalPredictor
Target: future_degradation

[cycle-001] Predictive warning / connected
  Future degradation:  0.033857
  Risk level:          LOW
  ...

[cycle-002] Connectivity loss / local resilience
  Future degradation:  0.003141
  Risk level:          NORMAL
  Local buffering:     True
  ...

[cycle-003] Connectivity recovery / synchronization
  Future degradation:  0.043561
  Risk level:          MEDIUM
  Recovery detected:   True
  Sync ready:          True

DEMO SCENARIO: PASS
```

---

## 3. Generate V4 evidence artifact

```
python scripts\generate_v4_demo_evidence.py
```

Output: `data/evidence/v4_demo_scenario.json`

---

## 4. Start the dashboard

```
python src\dashboard\server.py
```

Then open: http://127.0.0.1:8765

The dashboard shows the three-cycle V4 scenario with:
- Predicted future degradation
- Risk level (color coded)
- Connectivity state
- Buffering / recovery / sync status
- Model provenance
- Deployment status
- Safety boundary footer

---

## 5. Verify the evidence API

With the dashboard running, open: http://127.0.0.1:8765/api/evidence

This returns the raw `v4_demo_scenario.json` as JSON.

---

## 6. Run the deployment audit

```
python -c "
import json
from pathlib import Path
m = json.loads(Path('experiments/snapdragon_deployment_manifest_v4.json').read_text())
print('Status:', m['status'])
for b in m['backends']:
    print(f'  {b[\"name\"]}: verified={b[\"verified\"]}')
print('Snapdragon hardware verified:', m['snapdragon_hardware']['verified'])
"
```

Expected:

```
Status: CPU_AND_ONNX_VALIDATED_SNAPDRAGON_PENDING
  cpu_reference: verified=True
  onnx: verified=True
  qualcomm_qnn: verified=False
Snapdragon hardware verified: False
```

---

## 7. Verify protected artifact checksums

```
python -c "
import hashlib, json
from pathlib import Path

def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

ckpt = sha256('models/edgeresilience/temporal_predictor_v4.pt')
print('V4 checkpoint SHA256:', ckpt)
print('Expected:            ', 'b551ad9f02b56668ef3f8f7873133748275307f1934ec7fd77da14e7325d26b9')
print('Match:', ckpt == 'b551ad9f02b56668ef3f8f7873133748275307f1934ec7fd77da14e7325d26b9')
"
```

---

## Key artifact paths

| Artifact | Path |
|---|---|
| V4 checkpoint | models/edgeresilience/temporal_predictor_v4.pt |
| V4 dynamic ONNX | models/edgeresilience/temporal_predictor_v4_dynamic.onnx |
| V4 dataset | data/processed/temporal/edgeresilience_temporal_dataset_v4.jsonl |
| V4 demo evidence | data/evidence/v4_demo_scenario.json |
| Deployment manifest | experiments/snapdragon_deployment_manifest_v4.json |
| Training report | models/edgeresilience/temporal_predictor_v4_report.json |

---

## Safety boundary

This is a software simulation / virtual laboratory.

- Physical vehicle test: NO
- External CAN transmission: NO
- Direct actuation: NO
- Snapdragon hardware: NOT VERIFIED
- Qualcomm QNN: NOT VERIFIED
