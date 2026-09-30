from pathlib import Path
import numpy as np
import onnxruntime as ort

ROOT = Path(r"E:\EdgeResilience")

model = ROOT / "experiments" / "v4_output_head_fc1_diagnostic.onnx"
xfile = ROOT / "experiments" / "v4_output_head_control_input.npy"
outfile = ROOT / "experiments" / "v4_output_head_fc1_cpu_output.npy"

x = np.load(xfile).astype(np.float32)

session = ort.InferenceSession(
    str(model),
    providers=["CPUExecutionProvider"]
)

inp = session.get_inputs()[0].name
out = session.get_outputs()[0].name

y = session.run([out], {inp: x})[0].astype(np.float32)

np.save(outfile, y)

print("INPUT:", inp)
print("INPUT SHAPE:", x.shape)
print("OUTPUT:", out)
print("OUTPUT SHAPE:", y.shape)
print("CPU FC1 first 8:", y.reshape(-1)[:8])
print("CPU FC1 min:", float(y.min()))
print("CPU FC1 max:", float(y.max()))
print("CPU FC1 mean:", float(y.mean()))
print("CPU FC1 std:", float(y.std()))
print("SAVED:", outfile)
