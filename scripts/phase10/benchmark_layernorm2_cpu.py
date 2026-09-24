import numpy as np
import onnxruntime as ort
from pathlib import Path

model = Path(r"E:\EdgeResilience\models\edgeresilience\snapdragon\v4_diag_layernorm2.onnx")
inputs_path = Path(r"E:\EdgeResilience\artifacts\phase10\qualcomm_inference\v4_multi_hw_inputs.npz")
output_path = Path(r"E:\EdgeResilience\artifacts\phase10\qualcomm_inference\cpu_layernorm2_outputs.npy")

data = np.load(inputs_path)

session = ort.InferenceSession(
    str(model),
    providers=["CPUExecutionProvider"]
)

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

print("Input :", input_name)
print("Output:", output_name)

outputs = []

for i, key in enumerate(data.files):
    x = data[key].astype(np.float32)
    y = session.run([output_name], {input_name: x})[0]

    print(
        f"CASE {i}:",
        "shape=", y.shape,
        "dtype=", y.dtype,
        "min=", float(y.min()),
        "max=", float(y.max()),
        "mean=", float(y.mean()),
        "std=", float(y.std())
    )

    outputs.append(y)

outputs = np.stack(outputs, axis=0)

np.save(output_path, outputs)

print()
print("Saved:", output_path)
print("Shape:", outputs.shape)
print("Dtype:", outputs.dtype)
