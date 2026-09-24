import onnx
from onnx import helper, TensorProto, numpy_helper
import numpy as np

X = helper.make_tensor_value_info(
    "x", TensorProto.FLOAT, [1, 12, 64]
)

Y = helper.make_tensor_value_info(
    "y", TensorProto.FLOAT, [1, 12, 64]
)

scale = numpy_helper.from_array(
    np.ones(64, dtype=np.float32),
    name="scale"
)

bias = numpy_helper.from_array(
    np.zeros(64, dtype=np.float32),
    name="bias"
)

node = helper.make_node(
    "LayerNormalization",
    ["x", "scale", "bias"],
    ["y"],
    name="v4_layernorm_control",
    axis=-1,
    epsilon=1e-5,
    stash_type=1,
)

graph = helper.make_graph(
    [node],
    "V4LayerNormQNNControl",
    [X],
    [Y],
    initializer=[scale, bias],
)

model = helper.make_model(
    graph,
    producer_name="EdgeResilience",
    ir_version=10,
    opset_imports=[helper.make_opsetid("", 17)],
)

onnx.checker.check_model(model, full_check=True)

out = r".\models\edgeresilience\snapdragon\v4_layernorm_qnn_control.onnx"
onnx.save_model(model, out)

print("created:", out)
print("IR:", model.ir_version)
print("opset:", model.opset_import[0].version)
print("input:", "[1,12,64]")
print("axis:", -1)
print("epsilon:", 1e-5)
print("stash_type:", 1)
