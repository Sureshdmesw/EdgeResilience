from pathlib import Path
import numpy as np
import onnxruntime as ort
import hashlib
import json

ROOT = Path(r"E:\EdgeResilience")

input_path = ROOT / "experiments" / "v4_snapdragon_control_input.npy"
model_path = ROOT / "models" / "edgeresilience" / "snapdragon" / "temporal_predictor_v4_qnn_ready.onnx"
output_path = ROOT / "experiments" / "v4_snapdragon_cpu_reference.json"

x = np.load(input_path).astype(np.float32)

print("INPUT:", input_path)
print("INPUT SHAPE:", x.shape)
print("INPUT DTYPE:", x.dtype)
print("INPUT SHA256:", hashlib.sha256(x.tobytes()).hexdigest())

session = ort.InferenceSession(
    str(model_path),
    providers=["CPUExecutionProvider"],
)

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

y = session.run(
    [output_name],
    {input_name: x},
)[0]

print("MODEL INPUT :", input_name)
print("MODEL OUTPUT:", output_name)
print("CPU OUTPUT SHAPE:", y.shape)
print("CPU OUTPUT:", y)

result = {
    "model": str(model_path),
    "input_file": str(input_path),
    "input_sha256": hashlib.sha256(x.tobytes()).hexdigest(),
    "input_shape": list(x.shape),
    "input_dtype": str(x.dtype),
    "output_name": output_name,
    "output_shape": list(y.shape),
    "cpu_output": np.asarray(y).reshape(-1).tolist(),
}

output_path.write_text(
    json.dumps(result, indent=2),
    encoding="utf-8",
)

print("REFERENCE:", output_path)
