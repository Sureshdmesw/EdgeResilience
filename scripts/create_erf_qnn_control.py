import onnx
from onnx import helper, TensorProto

X = helper.make_tensor_value_info(
    "x", TensorProto.FLOAT, [1, 16]
)

Y = helper.make_tensor_value_info(
    "y", TensorProto.FLOAT, [1, 16]
)

node = helper.make_node(
    "Erf",
    ["x"],
    ["y"],
    name="erf_control"
)

graph = helper.make_graph(
    [node],
    "ErfQNNControl",
    [X],
    [Y]
)

model = helper.make_model(
    graph,
    producer_name="EdgeResilience",
    ir_version=10,
    opset_imports=[helper.make_opsetid("", 17)]
)

onnx.checker.check_model(model, full_check=True)

out = r".\models\edgeresilience\snapdragon\erf_qnn_control.onnx"
onnx.save_model(model, out)

print("created:", out)
print("IR:", model.ir_version)
