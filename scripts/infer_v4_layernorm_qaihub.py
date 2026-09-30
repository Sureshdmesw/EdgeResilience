from pathlib import Path
import hashlib
import numpy as np
import qai_hub as hub
import json

ROOT = Path(r"E:\EdgeResilience")

input_path = ROOT / "experiments" / "v4_output_head_control_input.npy"
cpu_path = ROOT / "experiments" / "v4_layernorm_cpu_output.npy"

x = np.load(input_path).astype(np.float32)
cpu = np.load(cpu_path).astype(np.float32)

print("INPUT SHAPE:", x.shape)
print("INPUT SHA256:", hashlib.sha256(x.tobytes()).hexdigest())

print("CPU OUTPUT SHAPE:", cpu.shape)
print("CPU FIRST 8:", cpu[0, :8])

compile_job = hub.get_job("jgolj6e1g")
target_model = compile_job.get_target_model()

device = hub.Device("Snapdragon X Elite CRD")

inputs = {
    "/ReduceSum_output_0": [x]
}

job = hub.submit_inference_job(
    model=target_model,
    device=device,
    inputs=inputs,
    name="EdgeResilience V4 LayerNorm Controlled Inference",
)

print("INFERENCE JOB:", job.job_id)

job.wait()

print("INFERENCE COMPLETE")

output_data = job.download_output_data()

print("OUTPUT DATA:", output_data)

if output_data is None:
    raise RuntimeError("Inference returned no output data")

value = next(iter(output_data.values()))
snap = np.asarray(value[0] if isinstance(value, list) else value).astype(np.float32)

print("SNAPDRAGON OUTPUT SHAPE:", snap.shape)
print("SNAPDRAGON FIRST 8:", snap[0, :8])

diff = snap - cpu

print("MAX ABS ERROR:", float(np.max(np.abs(diff))))
print("MEAN ABS ERROR:", float(np.mean(np.abs(diff))))
print("RMSE:", float(np.sqrt(np.mean(diff ** 2))))
print("SNAP MIN:", float(snap.min()))
print("SNAP MAX:", float(snap.max()))
print("SNAP MEAN:", float(snap.mean()))
print("SNAP STD:", float(snap.std()))

np.save(ROOT / "experiments" / "v4_layernorm_snapdragon_output.npy", snap)
