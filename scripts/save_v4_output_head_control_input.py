from pathlib import Path
import numpy as np
import onnxruntime as ort
import hashlib

ROOT = Path(r"E:\EdgeResilience")

model = ROOT / "experiments" / "v4_qnn_ready_diagnostic.onnx"
input_file = ROOT / "experiments" / "v4_snapdragon_control_input.npy"
output_file = ROOT / "experiments" / "v4_output_head_control_input.npy"

x = np.load(input_file).astype(np.float32)

session = ort.InferenceSession(
    str(model),
    providers=["CPUExecutionProvider"],
)

outputs = session.run(
    ["/ReduceSum_output_0"],
    {"vehicle_temporal_features": x},
)

control = np.asarray(outputs[0], dtype=np.float32)

np.save(output_file, control)

print("SAVED:", output_file)
print("SHAPE:", control.shape)
print("DTYPE:", control.dtype)
print("SHA256:", hashlib.sha256(control.tobytes()).hexdigest())
print("FIRST 8:", control.reshape(-1)[:8])
