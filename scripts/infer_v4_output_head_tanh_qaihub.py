from pathlib import Path
import hashlib
import numpy as np
import qai_hub as hub

ROOT = Path(r"E:\EdgeResilience")

input_path = ROOT / "experiments" / "v4_output_head_control_input.npy"

x = np.load(input_path).astype(np.float32)

print("INPUT SHAPE:", x.shape)
print("INPUT DTYPE:", x.dtype)
print("INPUT SHA256:", hashlib.sha256(x.tobytes()).hexdigest())

# Recover the successful compile job.
compile_job = hub.get_job("jp2r2ylqg")

target_model = compile_job.get_target_model()

print("COMPILE JOB:", compile_job.job_id)
print("TARGET MODEL:", target_model)
print("TARGET MODEL ID:", target_model.model_id)
print("TARGET MODEL TYPE:", type(target_model).__name__)

device = hub.Device("Snapdragon X Elite CRD")

inputs = {
    "/ReduceSum_output_0": [x]
}

job = hub.submit_inference_job(
    model=target_model,
    device=device,
    inputs=inputs,
    name="EdgeResilience V4 Output Head Tanh GELU Controlled Inference",
)

print("INFERENCE JOB:", job)
print("JOB ID:", job.job_id)

job.wait()

print("INFERENCE COMPLETE")

output_data = job.download_output_data()

print("OUTPUT DATA:", output_data)

for key, value in output_data.items():
    print("OUTPUT KEY:", key)

    if isinstance(value, np.ndarray):
        y = value
    else:
        y = np.asarray(value)

    print("SNAPDRAGON TANH-GELU OUTPUT:", y)
    break


