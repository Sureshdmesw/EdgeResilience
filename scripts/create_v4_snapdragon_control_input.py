from pathlib import Path
import numpy as np

ROOT = Path(r"E:\EdgeResilience")
path = ROOT / "experiments" / "v4_snapdragon_control_input.npy"

rng = np.random.default_rng(20260930)
x = rng.standard_normal((1, 12, 17)).astype(np.float32)

np.save(path, x)

print("INPUT:", path)
print("SHAPE:", x.shape)
print("DTYPE:", x.dtype)
print("SHA256:", __import__("hashlib").sha256(x.tobytes()).hexdigest())
print("MIN:", x.min())
print("MAX:", x.max())
print("MEAN:", x.mean())
print("STD:", x.std())
