from pathlib import Path
import onnx
from onnx import numpy_helper
import numpy as np

ROOT = Path(r"E:\EdgeResilience")

model = onnx.load(
    str(ROOT / "experiments" / "v4_layernorm_diagnostic.onnx")
)

init = {x.name: x for x in model.graph.initializer}

w = numpy_helper.to_array(init["ln_weight"]).astype(np.float32)
b = numpy_helper.to_array(init["ln_bias"]).astype(np.float32)

x = np.load(
    ROOT / "experiments" / "v4_output_head_control_input.npy"
).astype(np.float32)

cpu = np.load(
    ROOT / "experiments" / "v4_layernorm_cpu_output.npy"
).astype(np.float32)

snap = np.load(
    ROOT / "experiments" / "v4_layernorm_snapdragon_output.npy"
).astype(np.float32
)

# -----------------------------
# FP32 reference calculation
# -----------------------------
mean32 = np.mean(x, axis=-1, keepdims=True)
centered32 = x - mean32
var32 = np.mean(centered32 ** 2, axis=-1, keepdims=True)

y32 = (
    centered32
    / np.sqrt(var32 + np.float32(1e-5))
) * w + b

# -----------------------------
# FP16 arithmetic simulation
# -----------------------------
x16 = x.astype(np.float16)
w16 = w.astype(np.float16)
b16 = b.astype(np.float16)

mean16 = np.mean(
    x16,
    axis=-1,
    keepdims=True,
    dtype=np.float16,
)

centered16 = (
    x16 - mean16
).astype(np.float16)

sq16 = (
    centered16 * centered16
).astype(np.float16)

var16 = np.mean(
    sq16,
    axis=-1,
    keepdims=True,
    dtype=np.float16,
)

eps16 = np.float16(1e-5)

den16 = np.sqrt(
    (var16 + eps16).astype(np.float16)
).astype(np.float16)

norm16 = (
    centered16 / den16
).astype(np.float16)

y16 = (
    norm16 * w16 + b16
).astype(np.float16)

y16f = y16.astype(np.float32)

def report(name, reference, test):
    diff = test - reference

    print()
    print("===", name, "===")
    print("MAX ABS:", float(np.max(np.abs(diff))))
    print("MEAN ABS:", float(np.mean(np.abs(diff))))
    print("RMSE:", float(np.sqrt(np.mean(diff ** 2))))
    print("FIRST 8:", test[0, :8])

print("CPU FIRST 8:")
print(cpu[0, :8])

print()
print("SNAPDRAGON FIRST 8:")
print(snap[0, :8])

print()
print("FP16 SIM FIRST 8:")
print(y16f[0, :8])

report(
    "FP32 REFERENCE vs CPU",
    y32,
    cpu,
)

report(
    "FP32 REFERENCE vs SNAPDRAGON",
    y32,
    snap,
)

report(
    "FP16 SIMULATION vs SNAPDRAGON",
    y16f,
    snap,
)

report(
    "FP16 SIMULATION vs CPU",
    y16f,
    cpu,
)

np.save(
    ROOT / "experiments" / "v4_layernorm_fp16_sim_output.npy",
    y16f,
)

print()
print("SAVED:")
print(
    ROOT / "experiments" /
    "v4_layernorm_fp16_sim_output.npy"
)
