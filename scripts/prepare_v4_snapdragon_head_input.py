import numpy as np
from pathlib import Path

src = Path(r"experiments\v4_snapdragon_boundary_full.npy")
dst = Path(r"experiments\v4_snapdragon_boundary_head_input.npy")

x = np.load(src).astype(np.float32)

if x.shape != (1, 64):
    raise RuntimeError(f"Expected (1,64), got {x.shape}")

np.save(dst, x)

print("CREATED:", dst)
print("SHAPE:", x.shape)
print("DTYPE:", x.dtype)
print("MIN:", float(x.min()))
print("MAX:", float(x.max()))
print("MEAN:", float(x.mean()))
print("STD:", float(x.std()))
