import onnx
from onnx import helper, TensorProto, numpy_helper
import numpy as np

X = helper.make_tensor_value_info("x", TensorProto.FLOAT, [1, 16])

Y = helper.make_tensor_value_info("y", TensorProto.FLOAT, [1, 16])

scale = numpy_helper.from_array(
    np.ones(16, dtype=np.float32),
    name="scale"
)

bias = numpy_helper.from_array(
    np.zeros(16, dtype=np.float32),
    name="bias"
)

node = helper.make_node(
    "LayerNormalization",
    ["x", "scale", "bias"],
    ["y"],
    name="layernorm_control",
    axis=-1,
    epsilon=1e-5,
)

graph = helper.make_graph(
    [node],
    "LayerNormQNNControl",
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

out = r".\models\edgeresilience\snapdragon\layernorm_qnn_control.onnx"
onnx.save_model(model, out)

print("created:", out)
print("IR:", model.ir_version)
print("opset:", model.opset_import[0].version)
