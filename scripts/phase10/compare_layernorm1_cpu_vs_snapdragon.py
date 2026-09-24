import h5py
import numpy as np
from pathlib import Path

cpu_path = Path(r"E:\EdgeResilience\artifacts\phase10\qualcomm_inference\cpu_layernorm1_outputs.npy")
hw_path = Path(r"E:\EdgeResilience\artifacts\phase10\qualcomm_inference\layernorm1_snapdragon\dataset-d930oy5p9.h5")

cpu = np.load(cpu_path)

hw_cases = []
with h5py.File(hw_path, "r") as f:
    for i in range(5):
        hw_cases.append(np.array(f[f"data/0/batch_{i}"]))

hw = np.stack(hw_cases, axis=0)

print("CPU shape:", cpu.shape, cpu.dtype)
print("HW shape :", hw.shape, hw.dtype)

print()
print("CASE | MAX_ABS_ERROR | MEAN_ABS_ERROR | RMSE")
print("-" * 58)

all_diff = []

for i in range(5):
    diff = np.abs(cpu[i] - hw[i])
    rmse = np.sqrt(np.mean((cpu[i] - hw[i]) ** 2))

    print(
        f"{i:4d} | "
        f"{diff.max():.10f} | "
        f"{diff.mean():.10f} | "
        f"{rmse:.10f}"
    )

    all_diff.append(cpu[i] - hw[i])

all_diff = np.concatenate([x.reshape(-1) for x in all_diff])

print()
print("AGGREGATE")
print("MAX_ABS :", f"{np.max(np.abs(all_diff)):.10f}")
print("MEAN_ABS:", f"{np.mean(np.abs(all_diff)):.10f}")
print("RMSE    :", f"{np.sqrt(np.mean(all_diff ** 2)):.10f}")

print()
print("CPU case 0 stats:")
print(" min =", cpu[0].min())
print(" max =", cpu[0].max())
print(" mean=", cpu[0].mean())
print(" std =", cpu[0].std())

print()
print("HW case 0 stats:")
print(" min =", hw[0].min())
print(" max =", hw[0].max())
print(" mean=", hw[0].mean())
print(" std =", hw[0].std())
