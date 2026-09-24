import os
import numpy as np
import qai_hub as hub

PROJECT = r"E:\EdgeResilience"
OUT_DIR = os.path.join(PROJECT, "artifacts", "phase10", "qualcomm_inference")
os.makedirs(OUT_DIR, exist_ok=True)

# Five deterministic test cases
inputs = [
    np.zeros((1, 12, 64), dtype=np.float32),
    np.ones((1, 12, 64), dtype=np.float32),
    np.full((1, 12, 64), 0.5, dtype=np.float32),
    np.linspace(-1.0, 1.0, 12 * 64, dtype=np.float32).reshape(1, 12, 64),
    np.sin(np.arange(12 * 64, dtype=np.float32) * 0.1).reshape(1, 12, 64),
]

input_path = os.path.join(OUT_DIR, "v4_multi_hw_inputs.npz")
np.savez(input_path, *inputs)

print("=" * 70)
print("QUALCOMM V4 MULTI-INPUT NUMERICAL VALIDATION")
print("=" * 70)

for i, x in enumerate(inputs):
    print(f"Input {i}: shape={x.shape}, min={x.min():.7f}, max={x.max():.7f}")

client = hub.Client()
model = client.get_model("mq9y70pln")
device = hub.Device("Snapdragon X Elite CRD")

print("\nSubmitting multi-input Snapdragon inference...")

job = client.submit_inference_job(
    model=model,
    device=device,
    inputs={"add_3": inputs},
    name="EdgeResilience V4 Snapdragon Multi Input Numerical Validation",
)

print(f"Job ID: {job.job_id}")
print(f"Job URL: {job.url}")

print("\nWaiting for completion...")
status = job.wait()

print(f"Final status: {status}")

if getattr(status, "code", None) is not None and str(status.code) != "SUCCESS":
    raise RuntimeError(f"Qualcomm inference failed: {status}")

print("\nDownloading outputs...")
outputs = job.download_output_data()

print("Output keys:", list(outputs.keys()))

for name, value in outputs.items():
    value = np.asarray(value)
    print(f"\n{name}")
    print("Shape:", value.shape)
    print("Values:")
    print(value)

    np.save(
        os.path.join(OUT_DIR, f"multi_snapdragon_{name}.npy"),
        value
    )

print("\nMULTI-INPUT INFERENCE COMPLETE")
