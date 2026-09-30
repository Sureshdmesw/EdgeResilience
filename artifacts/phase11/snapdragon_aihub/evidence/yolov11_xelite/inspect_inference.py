import h5py
import numpy as np
import onnxruntime as ort

h = r"artifacts\phase11\snapdragon_aihub\evidence\yolov11_xelite\inference_j56886mvg.h5"

with h5py.File(h, "r") as f:
    sb = f["data/0/batch_0"][:]
    ss = f["data/1/batch_0"][:]
    sc = f["data/2/batch_0"][:]

m = r"artifacts\phase11\snapdragon_aihub\compile\yolov11_xelite\extracted\job_j5wlly94p_optimized_onnx\model.onnx"

sess = ort.InferenceSession(m, providers=["CPUExecutionProvider"])
cb, cs, cc = sess.run(
    None,
    {"image": np.zeros((1, 3, 640, 640), dtype=np.float32)}
)

print("=== CPU ===")
print("boxes min/max:", cb.min(), cb.max())
print("scores min/max:", cs.min(), cs.max())
print("classes:", np.unique(cc, return_counts=True))

print("\n=== SNAPDRAGON ===")
print("boxes min/max:", sb.min(), sb.max())
print("scores min/max:", ss.min(), ss.max())
print("classes:", np.unique(sc, return_counts=True))

print("\n=== SCORE THRESHOLDS ===")
for t in [0, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.1, 0.5]:
    print(
        t,
        "CPU count", int(np.sum(cs > t)),
        "SNAP count", int(np.sum(ss > t))
    )
