import onnx
from pathlib import Path

src = Path(r"E:\EdgeResilience\models\edgeresilience\snapdragon\v4_temporal_pooling_plus_head_qnn_control_clean.onnx")
dst = Path(r"E:\EdgeResilience\models\edgeresilience\snapdragon\v4_diag_layernorm2.onnx")

m = onnx.load(src)

target = "layer_norm_4"

# Find the target tensor in value_info
matches = [v for v in m.graph.value_info if v.name == target]

if not matches:
    raise RuntimeError(f"Target tensor not found in value_info: {target}")

# Replace the existing graph output with layer_norm_4
old_output = m.graph.output[0]
new_output = onnx.helper.make_tensor_value_info(
    target,
    old_output.type.tensor_type.elem_type,
    [1, 64]
)

del m.graph.output[:]
m.graph.output.append(new_output)

# Remove duplicate value_info because target is now graph output
kept = [v for v in m.graph.value_info if v.name != target]

del m.graph.value_info[:]
m.graph.value_info.extend(kept)

onnx.checker.check_model(m)
onnx.save(m, dst)

print("Created:", dst)
print("Input :", m.graph.input[0].name)
print("Output:", m.graph.output[0].name)
print("Output shape:", [d.dim_value for d in m.graph.output[0].type.tensor_type.shape.dim])
print("ONNX CHECKER: PASS")
