# EdgeResilience — Demo Narrative

**Competition:** Qualcomm Snapdragon AI Lab Build and Present Challenge
**Demo duration:** 3–5 minutes
**Format:** Live dashboard + terminal output

---

## Setup (before presenting)

1. Run: `python scripts\generate_v4_demo_evidence.py`
2. Start: `python src\dashboard\server.py`
3. Open browser: http://127.0.0.1:8765
4. Have terminal ready to run: `python demo\run_demo.py`

---

## Narrative Script

---

### Opening (30 seconds)

"Connected vehicles face a growing cyber threat landscape — CAN bus injection,
timing manipulation, payload tampering. The challenge isn't just detecting
these threats. It's doing it locally, at the edge, even when the vehicle
loses connectivity to the cloud.

EdgeResilience solves this with a Temporal Transformer running at the edge,
predicting future resilience degradation before it becomes critical — and
maintaining that intelligence even when the network goes down."

---

### The Problem (30 seconds)

"Traditional approaches wait for an anomaly to occur and then react.
EdgeResilience predicts future degradation from a temporal window of
cyber telemetry observations — 17 features over 12 time steps — giving
the system time to prepare before a threat materializes.

And critically: when connectivity is lost, the system doesn't stop.
It keeps inferring locally, buffers tamper-evident evidence, and
synchronizes when the connection recovers."

---

### The Architecture (45 seconds)

[Point to dashboard or architecture diagram]

"The pipeline has five stages:

One — 17 cyber telemetry features over 12 observation steps feed into
the V4 Temporal Transformer.

Two — The model outputs a predicted future degradation score.

Three — A deterministic policy interprets that score into a risk level:
NORMAL, LOW, MEDIUM, HIGH, or CRITICAL.

Four — The connectivity module evaluates network state. If connectivity
is lost, local inference continues and evidence is buffered locally.

Five — When connectivity recovers, a synchronization manifest is prepared
from the buffered evidence records."

---

### The AI Model (30 seconds)

"The V4 model is a Temporal Transformer with 71,000 parameters.
It uses learned temporal attention pooling — each of the 12 observation
steps is weighted by its relevance to the prediction.

We validated this with an ablation study: the full 12-step sequence
achieves MAE of 0.0051 versus 0.0067 for final-step-only input.
Temporal trajectory information genuinely improves the prediction."

---

### Live Demo — Terminal (60 seconds)

[Run: `python demo\run_demo.py`]

"Let me run the three-cycle demonstration.

Cycle one: the vehicle is connected. The model predicts a degradation
of 0.034 — risk level LOW. Local inference is active. No buffering needed.

Cycle two: connectivity is lost. The model keeps running locally —
degradation 0.003, risk NORMAL. But notice: local buffering is now TRUE.
The evidence record is preserved locally with a SHA-256 digest.

Cycle three: connectivity recovers. Degradation rises to 0.044 — risk MEDIUM.
Recovery is detected. Synchronization is ready. The buffered evidence
can now be prepared for synchronization."

---

### Live Demo — Dashboard (30 seconds)

[Point to browser at http://127.0.0.1:8765]

"The dashboard shows the same scenario visually. Each cycle displays
the predicted degradation, risk level, connectivity state, and
synchronization status. The deployment banner shows our current status:
CPU and ONNX verified — Snapdragon pending hardware verification."

---

### Deployment Path (30 seconds)

"The model is exported to ONNX with dynamic batch support.
We've verified numerical equivalence across batch sizes 1, 4, and 16
with a maximum error of 5.96e-08.

On CPU, ONNX Runtime achieves approximately 5.88x lower latency than
PyTorch — that's a CPU-to-CPU measurement on an Intel Core i5.

The next step is Qualcomm QNN conversion and deployment on a Snapdragon
device. The ONNX model is ready. Hardware verification is pending."

---

### Snapdragon Opportunity (20 seconds)

"Snapdragon's NPU is the natural target for this workload.
A 71,000-parameter Transformer running at 12-step inference is well-suited
for NPU acceleration. The expected benefits are lower latency, lower power,
and thermal efficiency — all critical for always-on edge vehicle compute.

We will not claim those numbers until we measure them on actual hardware."

---

### Closing (20 seconds)

"EdgeResilience demonstrates a complete, validated edge AI pipeline:
predictive intelligence, local resilience, tamper-evident evidence,
and a clear Snapdragon deployment path.

The V4 baseline is validated. The ONNX deployment is verified.
The Snapdragon path is ready for hardware verification."

---

## Key Numbers to Cite

| Metric | Value | Source |
|---|---|---|
| Test MAE | 0.0051 | temporal_predictor_v4_report.json |
| Test RMSE | 0.0066 | temporal_predictor_v4_report.json |
| Temporal ablation improvement | 0.0067 -> 0.0052 MAE | v4_neural_ablation_report.json |
| ONNX CPU speedup | ~5.88x vs PyTorch | v4_pytorch_vs_onnx_cpu_benchmark.json |
| ONNX equivalence max error | 5.96e-08 | v4_dynamic_onnx_equivalence_report.json |
| Model parameters | 71,170 | temporal_predictor_v4_report.json |
| Dataset records | 5,000 | dataset manifest |

---

## What NOT to Say

- Do NOT say "runs on Snapdragon" — hardware not verified
- Do NOT say "NPU acceleration" — not measured
- Do NOT say "tested on real vehicle" — software simulation only
- Do NOT say "certified safety system" — demonstration policy only
- Do NOT say "real CAN bus" — virtual laboratory
- Do NOT say "5.88x Snapdragon speedup" — that is a CPU-to-CPU number
