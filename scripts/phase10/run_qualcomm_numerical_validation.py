import os
import numpy as np
import qai_hub as hub

PROJECT = r"E:\EdgeResilience"
INPUT_PATH = os.path.join(
    PROJECT, "artifacts", "phase10", "qualcomm_inference", "v4_hw_input.npy"
)
OUT_DIR = os.path.join(
    PROJECT, "artifacts", "phase10", "qualcomm_inference"
)

os.makedirs(OUT_DIR, exist_ok=True)

print("=" * 70)
print("QUALCOMM SNAPDRAGON V4 NUMERICAL VALIDATION")
print("=" * 70)

# Load deterministic input
x = np.load(INPUT_PATH).astype(np.float32)

print(f"Input path : {INPUT_PATH}")
print(f"Input shape: {x.shape}")
print(f"Input dtype: {x.dtype}")
print(f"Input min  : {x.min()}")
print(f"Input max  : {x.max()}")

# QAI Hub client
client = hub.Client()

# Target device
device = hub.Device("Snapdragon X Elite CRD")

print(f"\nDevice: {device}")

# Submit inference against the successful compiled target model
print("\nSubmitting Snapdragon inference job...")

job = client.submit_inference_job(
    model=client.get_model("mq9y70pln"),
    device=device,
    inputs={"add_3": [x]},
    name="EdgeResilience V4 Snapdragon Numerical Validation",
)

print(f"Job type: {type(job).__name__}")
print(f"Job URL : {job.url}")

print("\nWaiting for Snapdragon inference...")
status = job.wait()

print(f"Final status: {status}")

# Download output tensor
print("\nDownloading hardware output...")
outputs = job.download_output_data()

print(f"Output type: {type(outputs)}")
print(f"Output keys: {list(outputs.keys())}")

# Save outputs
for name, value in outputs.items():
    value = np.asarray(value)
    path = os.path.join(
        OUT_DIR,
        f"snapdragon_output_{name}.npy"
    )
    np.save(path, value)

    print(f"\n{name}")
    print(f"  shape: {value.shape}")
    print(f"  dtype: {value.dtype}")
    print(f"  value: {value}")
    print(f"  saved: {path}")

print("\nQUALCOMM INFERENCE SUBMISSION COMPLETE")
