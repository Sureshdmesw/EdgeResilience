import numpy as np
import qai_hub as hub
import json
from pathlib import Path

JOB_ID = "jpvlj1er5"

job = hub.get_job(JOB_ID)

print("JOB:", JOB_ID)
print("JOB TYPE:", type(job).__name__)

output_data = job.download_output_data()

print("OUTPUT KEYS:", list(output_data.keys()))

for name, values in output_data.items():
    arr = np.asarray(values)
    print(name, "shape=", arr.shape, "dtype=", arr.dtype)

boundary_key = "output_1"

if boundary_key not in output_data:
    raise RuntimeError(
        f"Expected {boundary_key}, found {list(output_data.keys())}"
    )

boundary = np.asarray(output_data[boundary_key], dtype=np.float32)

if boundary.shape != (1, 1, 64):
    raise RuntimeError(f"Unexpected boundary shape: {boundary.shape}")

boundary = boundary.reshape(1, 64)

npy_path = Path(r"experiments\v4_snapdragon_boundary_full.npy")
json_path = Path(r"experiments\v4_snapdragon_boundary_full.json")

np.save(npy_path, boundary)

data = {
    "source_inference_job": JOB_ID,
    "shape": list(boundary.shape),
    "dtype": str(boundary.dtype),
    "min": float(boundary.min()),
    "max": float(boundary.max()),
    "mean": float(boundary.mean()),
    "std": float(boundary.std()),
    "values": boundary.flatten().tolist()
}

json_path.write_text(json.dumps(data, indent=2))

print("\nSAVED:")
print(npy_path)
print(json_path)

print("\nFULL BOUNDARY:")
print(boundary)
