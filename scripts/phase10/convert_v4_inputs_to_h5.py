import numpy as np
import h5py
from pathlib import Path

src = Path(r"E:\EdgeResilience\artifacts\phase10\qualcomm_inference\v4_multi_hw_inputs.npz")
dst = Path(r"E:\EdgeResilience\artifacts\phase10\qualcomm_inference\v4_multi_hw_inputs.h5")

data = np.load(src)

print("NPZ keys:", list(data.keys()))

with h5py.File(dst, "w") as f:
    for key in data.files:
        arr = data[key]
        f.create_dataset(key, data=arr)
        print(key, arr.shape, arr.dtype)

print("Created:", dst)
