import numpy as np
import h5py
from pathlib import Path

src = Path(
    r"E:\EdgeResilience\artifacts\phase10\qualcomm_inference\v4_multi_hw_inputs.npz"
)

dst = Path(
    r"E:\EdgeResilience\artifacts\phase10\qualcomm_inference\v4_sum1_hw_inputs.h5"
)

d = np.load(src)

arrays = [
    d["arr_0"],
    d["arr_1"],
    d["arr_2"],
    d["arr_3"],
    d["arr_4"],
]

with h5py.File(dst, "w") as f:
    data = f.create_group("data")
    group = data.create_group("0")

    for i, arr in enumerate(arrays):
        group.create_dataset(
            f"batch_{i}",
            data=arr.astype(np.float32)
        )

print("Created:", dst)

with h5py.File(dst, "r") as f:
    for name in f["data"]["0"]:
        x = f["data"]["0"][name]
        print(name, x.shape, x.dtype)
