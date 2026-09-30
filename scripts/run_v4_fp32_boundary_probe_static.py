import numpy as np
import qai_hub as hub
import hashlib
from pathlib import Path

TARGET_COMPILE_JOB = "jp4yzxx8p"
INPUT_PATH = Path(r"experiments\v4_snapdragon_control_input.npy")

compile_job = hub.get_job(TARGET_COMPILE_JOB)
target_model = compile_job.get_target_model()

devices = hub.get_devices(name="Snapdragon X Elite CRD")
if not devices:
    raise RuntimeError("Snapdragon X Elite CRD not found")

device = devices[0]

x = np.load(INPUT_PATH).astype(np.float32)

print("TARGET MODEL:", target_model.model_id)
print("DEVICE:", device)
print("INPUT SHAPE:", x.shape)
print("INPUT DTYPE:", x.dtype)
print("INPUT ARRAY SHA256:", hashlib.sha256(x.tobytes()).hexdigest())

job = hub.submit_inference_job(
    model=target_model,
    device=device,
    inputs={
        "vehicle_temporal_features": [x]
    },
    name="v4-fp32-boundary-probe-inference"
)

print("INFERENCE JOB:", job.job_id)

job.wait()

print("INFERENCE COMPLETE")

output_data = job.download_output_data()

print("OUTPUT KEYS:", list(output_data.keys()))

for name, values in output_data.items():
    arr = np.asarray(values)
    print("\nOUTPUT:", name)
    print("SHAPE:", arr.shape)
    print("DTYPE:", arr.dtype)
    print("VALUES:", arr.flatten()[:16])
