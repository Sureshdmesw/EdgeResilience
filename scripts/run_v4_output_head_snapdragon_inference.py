from pathlib import Path
import hashlib
import json
import numpy as np
import qai_hub as hub

ROOT = Path(r"E:\EdgeResilience")

INPUT = ROOT / "experiments" / "v4_output_head_control_input.npy"
REPORT = ROOT / "experiments" / "v4_output_head_snapdragon_result.json"

x = np.load(INPUT).astype(np.float32)

print("INPUT:", INPUT)
print("SHAPE:", x.shape)
print("DTYPE:", x.dtype)
print("SHA256:", hashlib.sha256(x.tobytes()).hexdigest())

target_model = hub.get_job("jp1nrzw7g").get_target_model()

print("TARGET MODEL:", target_model)

job = hub.submit_inference_job(
    model=target_model,
    device=hub.Device("Snapdragon X Elite CRD"),
    inputs={
        "/ReduceSum_output_0": [x]
    },
    name="EdgeResilience V4 Output Head Controlled Inference",
)

print("INFERENCE JOB:", job.job_id)

status = job.wait()

print("STATUS:")
print(status)

outputs = job.download_output_data()

print("OUTPUT KEYS:", outputs.keys())

y = np.asarray(
    outputs[list(outputs.keys())[0]],
    dtype=np.float64
).reshape(-1)

cpu_reference = np.array([0.00803131], dtype=np.float64)

error = np.abs(cpu_reference - y)

print()
print("=" * 70)
print("OUTPUT HEAD CPU <-> SNAPDRAGON")
print("=" * 70)
print("CPU        :", cpu_reference)
print("Snapdragon :", y)
print("ABS ERROR  :", error)
print("REL ERROR  :", error / np.maximum(np.abs(cpu_reference), 1e-12))
print("=" * 70)

report = {
    "compile_job": "jp1nrzw7g",
    "target_model": "mn75dgdvm",
    "inference_job": job.job_id,
    "device": "Snapdragon X Elite CRD",
    "input_sha256": hashlib.sha256(x.tobytes()).hexdigest(),
    "cpu_output": cpu_reference.tolist(),
    "snapdragon_output": y.tolist(),
    "absolute_error": error.tolist(),
}

REPORT.write_text(
    json.dumps(report, indent=2),
    encoding="utf-8",
)

print("REPORT:", REPORT)
