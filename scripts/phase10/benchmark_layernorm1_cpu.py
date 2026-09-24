import os
import numpy as np
import onnxruntime as ort

PROJECT = r"E:\EdgeResilience"
INPUTS = os.path.join(
    PROJECT, "artifacts", "phase10", "qualcomm_inference",
    "v4_multi_hw_inputs.npz"
)
MODEL = os.path.join(
    PROJECT, "models", "edgeresilience", "snapdragon",
    "v4_diag_layernorm1.onnx"
)
OUT = os.path.join(
    PROJECT, "artifacts", "phase10", "qualcomm_inference",
    "cpu_layernorm1_outputs.npy"
)

d = np.load(INPUTS)
session = ort.InferenceSession(
    MODEL,
    providers=["CPUExecutionProvider"]
)

outputs = []

for key in d.files:
    x = d[key].astype(np.float32)
    y = session.run(None, {"add_3": x})[0]
    outputs.append(y)

outputs = np.stack(outputs)

np.save(OUT, outputs)

print("=" * 70)
print("CPU FIRST-LAYERNORM REFERENCE")
print("=" * 70)
print("Shape:", outputs.shape)
print("Dtype:", outputs.dtype)
print("Saved:", OUT)

for i, y in enumerate(outputs):
    print(
        f"Case {i}: "
        f"min={y.min():.8f}, "
        f"max={y.max():.8f}, "
        f"mean={y.mean():.8f}, "
        f"std={y.std():.8f}"
    )
