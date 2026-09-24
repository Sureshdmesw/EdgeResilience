import numpy as np
import onnxruntime as ort
from pathlib import Path

model = Path(
    r"E:\EdgeResilience\models\edgeresilience\snapdragon\v4_diag_sum1_cpu.onnx"
)

inputs = Path(
    r"E:\EdgeResilience\artifacts\phase10\qualcomm_inference\v4_multi_hw_inputs.npz"
)

output = Path(
    r"E:\EdgeResilience\artifacts\phase10\qualcomm_inference\cpu_sum1_outputs.npy"
)

d = np.load(inputs)

session = ort.InferenceSession(
    str(model),
    providers=["CPUExecutionProvider"]
)

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

results = []

for i in range(5):
    x = d[f"arr_{i}"].astype(np.float32)
    y = session.run(
        [output_name],
        {input_name: x}
    )[0]
    results.append(y)

results = np.stack(results)

np.save(output, results)

print("Input name :", input_name)
print("Output name:", output_name)
print("Output shape:", results.shape)
print("Output dtype :", results.dtype)
print("Saved:", output)

for i, y in enumerate(results):
    print(
        f"CASE {i}: "
        f"min={y.min():.8f} "
        f"max={y.max():.8f} "
        f"mean={y.mean():.8f} "
        f"std={y.std():.8f}"
    )
