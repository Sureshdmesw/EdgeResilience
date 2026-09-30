from pathlib import Path
import hashlib
import json
import numpy as np
import qai_hub as hub

ROOT = Path(r"E:\EdgeResilience")

INPUT = ROOT / "experiments" / "v4_snapdragon_control_input.npy"
CPU_REF = ROOT / "experiments" / "v4_snapdragon_cpu_reference.json"
REPORT = ROOT / "experiments" / "v4_snapdragon_control_inference.json"

x = np.load(INPUT).astype(np.float32)

input_sha256 = hashlib.sha256(x.tobytes()).hexdigest()

print("INPUT:", INPUT)
print("SHAPE:", x.shape)
print("DTYPE:", x.dtype)
print("SHA256:", input_sha256)

with open(CPU_REF, "r", encoding="utf-8") as f:
    cpu_reference = json.load(f)

cpu_value = np.asarray(
    cpu_reference["cpu_output"],
    dtype=np.float64
).reshape(-1)

print("CPU REFERENCE:", cpu_value)

target_model = hub.get_job("jp1n962kg").get_target_model()

job = hub.submit_inference_job(
    model=target_model,
    device=hub.Device("Snapdragon X Elite CRD"),
    inputs={
        "vehicle_temporal_features": [x]
    },
    name="EdgeResilience V4 Controlled Snapdragon Inference",
)

print("INFERENCE JOB:", job.job_id)

status = job.wait()

print("STATUS:")
print(status)

outputs = job.download_output_data()

print("OUTPUT KEYS:", outputs.keys())

snapdragon_value = np.asarray(
    outputs[list(outputs.keys())[0]],
    dtype=np.float64
).reshape(-1)

print("SNAPDRAGON OUTPUT:", snapdragon_value)

abs_error = np.abs(cpu_value - snapdragon_value)

max_abs_error = float(np.max(abs_error))
mean_abs_error = float(np.mean(abs_error))
rmse = float(np.sqrt(np.mean((cpu_value - snapdragon_value) ** 2)))

print()
print("=" * 70)
print("CONTROLLED CPU <-> SNAPDRAGON COMPARISON")
print("=" * 70)
print("CPU        :", cpu_value)
print("Snapdragon :", snapdragon_value)
print("ABS ERROR  :", abs_error)
print("MAX ERROR  :", max_abs_error)
print("MEAN ERROR :", mean_abs_error)
print("RMSE       :", rmse)
print("=" * 70)

report = {
    "status": "SUCCESS",
    "inference_job": job.job_id,
    "compile_job": "jp1n962kg",
    "target_model": "mn75w5l8m",
    "device": "Snapdragon X Elite CRD",
    "input_file": str(INPUT),
    "input_sha256": input_sha256,
    "input_shape": list(x.shape),
    "input_dtype": str(x.dtype),
    "cpu_output": cpu_value.tolist(),
    "snapdragon_output": snapdragon_value.tolist(),
    "max_abs_error": max_abs_error,
    "mean_abs_error": mean_abs_error,
    "rmse": rmse,
}

REPORT.write_text(
    json.dumps(report, indent=2),
    encoding="utf-8",
)

print("REPORT:", REPORT)
