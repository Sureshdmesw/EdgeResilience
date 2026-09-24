import onnx
from onnx import helper, TensorProto, numpy_helper
import numpy as np

rng = np.random.default_rng(42)

W1 = rng.standard_normal((17, 16)).astype(np.float32)
B1 = rng.standard_normal((16,)).astype(np.float32)
W2 = rng.standard_normal((16, 1)).astype(np.float32)
B2 = rng.standard_normal((1,)).astype(np.float32)

X = helper.make_tensor_value_info(
    "features",
    TensorProto.FLOAT,
    [1, 17],
)

Y = helper.make_tensor_value_info(
    "score",
    TensorProto.FLOAT,
    [1, 1],
)

graph = helper.make_graph(
    [
        helper.make_node("Gemm", ["features", "W1", "B1"], ["hidden"], name="fc1"),
        helper.make_node("Relu", ["hidden"], ["activated"], name="relu"),
        helper.make_node("Gemm", ["activated", "W2", "B2"], ["logit"], name="fc2"),
        helper.make_node("Sigmoid", ["logit"], ["score"], name="sigmoid"),
    ],
    "TinyQNNControl",
    [X],
    [Y],
    [
        numpy_helper.from_array(W1, "W1"),
        numpy_helper.from_array(B1, "B1"),
        numpy_helper.from_array(W2, "W2"),
        numpy_helper.from_array(B2, "B2"),
    ],
)

model = helper.make_model(
    graph,
    producer_name="EdgeResilience",
    ir_version=10,
    opset_imports=[helper.make_opsetid("", 17)],
)

onnx.checker.check_model(model, full_check=True)

out = r".\models\edgeresilience\snapdragon\tiny_qnn_control_ir10.onnx"
onnx.save_model(model, out)

print("created:", out)
print("IR version:", model.ir_version)
print("opset:", [(x.domain, x.version) for x in model.opset_import])
print("nodes:", len(model.graph.node))
