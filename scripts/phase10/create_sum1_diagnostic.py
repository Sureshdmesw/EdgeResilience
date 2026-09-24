import onnx
from pathlib import Path

src = Path(
    r"E:\EdgeResilience\models\edgeresilience\snapdragon\v4_temporal_pooling_qnn_control.onnx"
)

dst = Path(
    r"E:\EdgeResilience\models\edgeresilience\snapdragon\v4_diag_sum1.onnx"
)

m = onnx.load(src)

target = "sum_1"

# Find the node that produces sum_1
producer = None
for node in m.graph.node:
    if target in node.output:
        producer = node
        break

if producer is None:
    raise RuntimeError(f"No node produces target tensor: {target}")

print("Producer:", producer.op_type)
print("Producer inputs:", list(producer.input))
print("Producer outputs:", list(producer.output))

# Infer tensor metadata from the graph
inferred = onnx.shape_inference.infer_shapes(m)

target_info = None

for v in inferred.graph.value_info:
    if v.name == target:
        target_info = v
        break

if target_info is None:
    raise RuntimeError(
        f"Shape inference did not produce metadata for: {target}"
    )

# Replace graph output with sum_1
del m.graph.output[:]
m.graph.output.append(target_info)

# Remove duplicate value_info
kept = [
    v for v in m.graph.value_info
    if v.name != target
]

del m.graph.value_info[:]
m.graph.value_info.extend(kept)

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
