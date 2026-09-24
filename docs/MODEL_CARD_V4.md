# EdgeResilience V4 — Model Card

---

## Model Details

| Property | Value |
|---|---|
| Model name | EdgeResilience_V4_TemporalPredictor |
| Model class | EdgeResilienceTemporalPredictor |
| Architecture | Temporal Transformer with attention pooling |
| Version | V4 |
| Checkpoint | models/edgeresilience/temporal_predictor_v4.pt |
| Checkpoint SHA256 | b551ad9f02b56668ef3f8f7873133748275307f1934ec7fd77da14e7325d26b9 |
| ONNX (dynamic) | models/edgeresilience/temporal_predictor_v4_dynamic.onnx |
| Parameters | 71,170 |
| Classification | New EdgeResilience artifact |

---

## Architecture

| Component | Configuration |
|---|---|
| Input projection | Linear(17, 64) |
| Positional embedding | Learned, [1, 12, 64] |
| Transformer encoder | 2 layers, 4 heads, d_model=64, ff=128, dropout=0.1, norm_first=True |
| Temporal attention pooling | Linear(64, 1) -> softmax over sequence -> weighted sum |
| Output head | LayerNorm(64) -> Linear(64, 32) -> GELU -> Dropout(0.1) -> Linear(32, 1) -> Sigmoid |

---

## Input

| Property | Value |
|---|---|
| Shape | [batch, 12, 17] |
| Dtype | float32 |
| Normalization | Z-score, parameters stored in checkpoint |
| Features | 17 EdgeResilience cyber/resilience features |
| Sequence length | 12 observation steps |

The 17 features are synthetic EdgeResilience cyber-physical scenario features.
They are NOT raw HCRL measurements.

---

## Output

| Property | Value |
|---|---|
| Shape | [batch] |
| Dtype | float32 |
| Range | [0, 1] (Sigmoid activation) |
| Interpretation | Predicted future resilience degradation |
| Target name | future_degradation |

---

## Training Data

| Property | Value |
|---|---|
| Dataset | edgeresilience_temporal_dataset_v4.jsonl |
| Records | 5,000 |
| Features | 17 per step |
| Steps | 12 |
| Generation | Synthetic EdgeResilience temporal scenarios |
| SHA256 | 02a82f0f5ee78dc4e3be28b81b53b6eb4eb884600a4734f3eb3aaa279cb3a911 |
| Latent regimes | Used during generation — NOT exposed as model features |

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
| Train / val / test split | 3200 / 800 / 1000 |
| Device | CPU |

---

## Performance

| Metric | V4 Model | Mean Baseline |
|---|---|---|
| Test MAE | 0.0051 | 0.0203 |
| Test RMSE | 0.0066 | 0.0232 |
| Best validation loss | 4.378e-05 | — |
| Beats mean baseline | YES | — |

---

## Temporal Ablation

| Input | MAE | RMSE |
|---|---|---|
| Final timestep only | 0.0067 | 0.0086 |
| Final + delta + std | 0.0053 | 0.0068 |
| Full 12-step sequence | 0.0052 | 0.0066 |

---

## Deployment Status

| Backend | Status |
|---|---|
| CPU reference (PyTorch) | VERIFIED |
| ONNX Runtime (CPU) | VERIFIED — ~5.88x vs PyTorch (CPU-to-CPU) |
| Qualcomm QNN | NOT VERIFIED |
| Snapdragon NPU | NOT VERIFIED |

---

## Intended Use

- Research and competition demonstration of edge AI for connected vehicle safety
- Predicting future cyber-physical resilience degradation from temporal telemetry
- Demonstrating local edge inference during connectivity loss
- Demonstrating evidence buffering and synchronization

---

## Non-Intended Use

- Production vehicle safety control
- Certified automotive safety system
- Direct vehicle actuation
- Real-time physical vehicle monitoring without additional validation
- Replacement for deterministic safety controls

---

## Limitations

1. Trained on synthetic data — not validated on real vehicle telemetry
2. Risk thresholds are demonstration defaults — not certified safety limits
3. Single-vehicle scenario — no multi-vehicle cooperative intelligence
4. Snapdragon hardware execution not yet verified
5. CPU training only — no GPU training performed
6. 5,000 training records — limited diversity compared to production datasets

---

## Safety Boundary

This model is part of a software simulation / virtual laboratory.

- Physical vehicle testing: NOT PERFORMED
- External CAN transmission: NOT PERFORMED
- Direct vehicle actuation: NOT PERFORMED
- Production vehicle connection: NOT PERFORMED

AI outputs are separated from deterministic safety policy.
The model does not directly command vehicle actuation.

---

## Provenance

This is a new EdgeResilience artifact trained from scratch.
It is NOT derived from the inherited frozen CRSS Transformer checkpoint.
It is NOT trained on raw HCRL measurements.
