import numpy as np
from pathlib import Path

ROOT = Path(r"E:\EdgeResilience")

x = np.array([[-4.816460674286316]], dtype=np.float32)

out = ROOT / "experiments" / "v4_fc2_snapdragon_exact_output.npy"

np.save(out, x)

print("FILE:", out)
print("SHAPE:", x.shape)
print("DTYPE:", x.dtype)
print("VALUE:", x)
print("SAVED")
