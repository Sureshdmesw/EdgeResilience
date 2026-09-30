from pathlib import Path
import numpy as np
import onnxruntime as ort
import json

ROOT = Path(r"E:\EdgeResilience")

model = ROOT / "experiments" / "v4_output_head_diagnostic.onnx"
snap_boundary = ROOT / "experiments" / "v4_reducesum_boundary_snapdragon_output.npy"

print("MODEL:", model)
print("BOUNDARY:", snap_boundary)

x = np.load(snap_boundary).astype(np.float32).reshape(1, 64)

print("INPUT SHAPE:", x.shape)
print("INPUT FIRST 8:")
print(x[0, :8])

session = ort.InferenceSession(
    str(model),
    providers=["CPUExecutionProvider"]
)

print()
print("MODEL INPUT:", session.get_inputs()[0].name)
print("MODEL OUTPUT:", session.get_outputs()[0].name)

result = session.run(
    None,
    {
        session.get_inputs()[0].name: x
    }
)[0]

result = np.asarray(result, dtype=np.float32)

print()
print("CPU HEAD OUTPUT:", result)
print("CPU HEAD SCALAR:", float(result.reshape(-1)[0]))

cpu_reference_file = ROOT / "experiments" / "v4_output_head_control_input.npy"

# CPU boundary → CPU head reference
cpu_boundary = np.load(cpu_reference_file).astype(np.float32).reshape(1, 64)

cpu_result = session.run(
    None,
    {
        session.get_inputs()[0].name: cpu_boundary
    }
)[0]

cpu_result = np.asarray(cpu_result, dtype=np.float32)

print()
print("CPU BOUNDARY → CPU HEAD:", cpu_result)
print("REFERENCE SCALAR:", float(cpu_result.reshape(-1)[0]))

snap_head = float(result.reshape(-1)[0])
cpu_head = float(cpu_result.reshape(-1)[0])

abs_error = abs(snap_head - cpu_head)
rel_error = abs_error / max(abs(cpu_head), 1e-12)

print()
print("=== CROSS-BOUNDARY TEST ===")
print("CPU BOUNDARY → CPU HEAD:", cpu_head)
print("SNAP BOUNDARY → CPU HEAD:", snap_head)
print("ABS ERROR:", abs_error)
print("RELATIVE ERROR:", rel_error)
print("RELATIVE ERROR %:", rel_error * 100)

report = {
    "cpu_boundary_cpu_head": cpu_head,
    "snapdragon_boundary_cpu_head": snap_head,
    "absolute_error": abs_error,
    "relative_error": rel_error,
    "relative_error_percent": rel_error * 100
}

report_file = ROOT / "experiments" / "v4_snap_boundary_cpu_head_result.json"

report_file.write_text(
    json.dumps(report, indent=2),
    encoding="utf-8"
)

print("REPORT:", report_file)
