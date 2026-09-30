from pathlib import Path
import json
import numpy as np
import onnxruntime as ort
import qai_hub as hub

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------
ROOT = Path(r"E:\EdgeResilience")

MODEL = ROOT / "models" / "edgeresilience" / "snapdragon" / "temporal_predictor_v4_qnn_ready.onnx"
REPORT = ROOT / "experiments" / "v4_cpu_snapdragon_numerical_equivalence.json"

# ------------------------------------------------------------
# Load the exact QNN-ready ONNX model
# ------------------------------------------------------------
session = ort.InferenceSession(
    str(MODEL),
    providers=["CPUExecutionProvider"],
)

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

print("ONNX INPUT :", input_name)
print("ONNX OUTPUT:", output_name)

# ------------------------------------------------------------
# Deterministic controlled input
# ------------------------------------------------------------
rng = np.random.default_rng(20260930)

x = rng.standard_normal((1, 12, 17)).astype(np.float32)

# CPU reference
cpu_output = session.run(
    [output_name],
    {input_name: x},
)[0]

print("CPU OUTPUT SHAPE:", cpu_output.shape)
print("CPU OUTPUT:", cpu_output)

# ------------------------------------------------------------
# QAI Hub compiled Snapdragon target
# ------------------------------------------------------------
compile_job = hub.get_job("jp1n962kg")
target_model = compile_job.get_target_model()

print("TARGET MODEL:", target_model)

# ------------------------------------------------------------
# Submit actual Snapdragon inference
# ------------------------------------------------------------
job = hub.submit_inference_job(
    model=target_model,
    device=hub.Device("Snapdragon X Elite CRD"),
    inputs={
        input_name: [x]
    },
    name="EdgeResilience V4 CPU Snapdragon Numerical Equivalence",
)

print("INFERENCE JOB:", job.job_id)

status = job.wait()
print("STATUS:", status)

# ------------------------------------------------------------
# Download Snapdragon output tensor
# ------------------------------------------------------------
outputs = job.download_output_data()

print("OUTPUT KEYS:", outputs.keys())

# QAI Hub returns a dictionary of output-name -> array/list
snapdragon_output = np.asarray(outputs[list(outputs.keys())[0]])

print("SNAPDRAGON OUTPUT SHAPE:", snapdragon_output.shape)
print("SNAPDRAGON OUTPUT:", snapdragon_output)

# ------------------------------------------------------------
# Numerical equivalence
# ------------------------------------------------------------
cpu = np.asarray(cpu_output, dtype=np.float64).reshape(-1)
snap = np.asarray(snapdragon_output, dtype=np.float64).reshape(-1)

if cpu.shape != snap.shape:
    raise RuntimeError(
        f"OUTPUT SHAPE MISMATCH: CPU={cpu.shape}, Snapdragon={snap.shape}"
    )

diff = np.abs(cpu - snap)

max_abs_error = float(np.max(diff))
mean_abs_error = float(np.mean(diff))
rmse = float(np.sqrt(np.mean((cpu - snap) ** 2)))

# Relative error with safe denominator
relative_error = diff / np.maximum(np.abs(cpu), 1e-12)

max_relative_error = float(np.max(relative_error))
mean_relative_error = float(np.mean(relative_error))

# Conservative acceptance threshold
MAX_ABS_TOL = 1e-4
MEAN_ABS_TOL = 1e-5

passed = (
    max_abs_error <= MAX_ABS_TOL
    and mean_abs_error <= MEAN_ABS_TOL
)

print()
print("=" * 70)
print("CPU <-> SNAPDRAGON NUMERICAL EQUIVALENCE")
print("=" * 70)
print(f"Max absolute error : {max_abs_error:.12e}")
print(f"Mean absolute error: {mean_abs_error:.12e}")
print(f"RMSE               : {rmse:.12e}")
print(f"Max relative error : {max_relative_error:.12e}")
print(f"Mean relative error: {mean_relative_error:.12e}")
print(f"Max tolerance      : {MAX_ABS_TOL:.1e}")
print(f"Mean tolerance     : {MEAN_ABS_TOL:.1e}")
print()
print("RESULT:", "PASS" if passed else "FAIL")
print("=" * 70)

# ------------------------------------------------------------
# Save evidence
# ------------------------------------------------------------
report = {
    "status": "PASS" if passed else "FAIL",
    "model": str(MODEL),
    "compile_job": "jp1n962kg",
    "target_model": "mn75w5l8m",
    "inference_job": job.job_id,
    "device": "Snapdragon X Elite CRD",
    "input_shape": list(x.shape),
    "output_shape": list(cpu.shape),
    "max_abs_error": max_abs_error,
    "mean_abs_error": mean_abs_error,
    "rmse": rmse,
    "max_relative_error": max_relative_error,
    "mean_relative_error": mean_relative_error,
    "max_abs_tolerance": MAX_ABS_TOL,
    "mean_abs_tolerance": MEAN_ABS_TOL,
}

REPORT.parent.mkdir(parents=True, exist_ok=True)

REPORT.write_text(
    json.dumps(report, indent=2),
    encoding="utf-8",
)

print()
print("REPORT:", REPORT)

if not passed:
    raise SystemExit(1)
