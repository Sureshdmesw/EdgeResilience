import numpy as np
import qai_hub as hub
from pathlib import Path

INPUT = Path(r"E:\EdgeResilience\experiments\v4_snapdragon_control_input.npy")

x = np.load(INPUT).astype(np.float32)

device = hub.Device(name="Snapdragon X Elite CRD")

compile_job = hub.get_job("jp4yzw12p")
compile_job.wait()

target_model = compile_job.get_target_model()

print("=== V4 FINAL + LAYERNORM TRACE INFERENCE ===")
print(f"Input: {INPUT}")
print(f"Shape: {x.shape}")
print(f"Dtype: {x.dtype}")
print(f"Compile Job: jp4yzw12p")
print(f"Target model: {target_model}")

job = hub.submit_inference_job(
    model=target_model,
    device=device,
    inputs={"vehicle_temporal_features": [x]},
)

print(f"Inference Job ID: {job.job_id}")

job.wait()

outputs = job.download_output_data()

print("\n=== OUTPUTS ===")
for name, values in outputs.items():
    arr = np.asarray(values[0])
    print(f"{name}: shape={arr.shape}, dtype={arr.dtype}")
    print(arr)
