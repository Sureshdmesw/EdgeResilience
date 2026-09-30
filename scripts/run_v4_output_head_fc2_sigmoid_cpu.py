from pathlib import Path
import numpy as np
import onnxruntime as ort

ROOT = Path(r"E:\EdgeResilience")

model = ROOT / "experiments" / "v4_output_head_fc2_sigmoid_diagnostic.onnx"
xfile = ROOT / "experiments" / "v4_output_head_gelu_cpu_output.npy"
outfile = ROOT / "experiments" / "v4_output_head_fc2_sigmoid_cpu_output.npy"

x = np.load(xfile).astype(np.float32)

session = ort.InferenceSession(
    str(model),
    providers=["CPUExecutionProvider"]
)

inp = session.get_inputs()[0].name
out = session.get_outputs()[0].name

print("INPUT:", inp)
print("INPUT SHAPE:", x.shape)
print("OUTPUT:", out)

y = session.run([out], {inp: x})[0].astype(np.float32)

np.save(outfile, y)

print()
print("CPU FC2+SIGMOID OUTPUT:", y)
print("CPU VALUE:", float(y.reshape(-1)[0]))
print("SAVED:", outfile)
