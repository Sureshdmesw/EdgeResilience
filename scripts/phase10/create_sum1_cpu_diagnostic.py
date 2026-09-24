import onnx
from pathlib import Path

src = Path(
    r"E:\EdgeResilience\models\edgeresilience\snapdragon\v4_temporal_pooling_qnn_control.onnx"
)

dst = Path(
    r"E:\EdgeResilience\models\edgeresilience\snapdragon\v4_diag_sum1_cpu.onnx"
)

m = onnx.load(src)
m = onnx.shape_inference.infer_shapes(m)

target = "sum_1"

target_info = None

for v in m.graph.value_info:
    if v.name == target:
        target_info = v
        break

if target_info is None:
    raise RuntimeError(f"Could not find inferred metadata for {target}")

# Replace graph output with sum_1
del m.graph.output[:]
m.graph.output.append(target_info)

# Remove sum_1 from value_info using protobuf-safe deletion
remove_indices = [
    i for i, v in enumerate(m.graph.value_info)
    if v.name == target
]

for i in reversed(remove_indices):
    del m.graph.value_info[i]

onnx.checker.check_model(m)
onnx.save(m, dst)

shape = [
    d.dim_value if d.HasField("dim_value") else "?"
    for d in target_info.type.tensor_type.shape.dim
]

print("Created:", dst)
print("Input :", m.graph.input[0].name)
print("Output:", m.graph.output[0].name)
print("Output shape:", shape)
print("ONNX CHECKER: PASS")
