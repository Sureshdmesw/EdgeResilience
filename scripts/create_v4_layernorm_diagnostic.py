from pathlib import Path
import onnx
from onnx import helper, TensorProto, numpy_helper
import numpy as np

ROOT = Path(r"E:\EdgeResilience")

src = ROOT / "experiments" / "v4_output_head_diagnostic.onnx"
dst = ROOT / "experiments" / "v4_layernorm_diagnostic.onnx"

model = onnx.load(str(src))
init = {x.name: x for x in model.graph.initializer}

w = numpy_helper.to_array(init["output_head.0.weight"]).astype(np.float32)
b = numpy_helper.to_array(init["output_head.0.bias"]).astype(np.float32)

input_name = "/ReduceSum_output_0"
output_name = "layernorm_output"

x = helper.make_tensor_value_info(
    input_name,
    TensorProto.FLOAT,
    [1, 64],
)

y = helper.make_tensor_value_info(
    output_name,
    TensorProto.FLOAT,
    [1, 64],
)

node = helper.make_node(
    "LayerNormalization",
    [input_name, "ln_weight", "ln_bias"],
    [output_name],
    name="LayerNorm",
    axis=-1,
    epsilon=1e-5,
)

graph = helper.make_graph(
    [node],
    "EdgeResilience_V4_LayerNorm_Diagnostic",
    [x],
    [y],
    initializer=[
        numpy_helper.from_array(w, "ln_weight"),
        numpy_helper.from_array(b, "ln_bias"),
    ],
)

diagnostic = helper.make_model(
    graph,
    producer_name="EdgeResilience",
    opset_imports=[helper.make_opsetid("", 17)],
)

diagnostic.ir_version = 10

onnx.checker.check_model(diagnostic)
onnx.save(diagnostic, str(dst))

print("CREATED:", dst)
print("INPUT:", input_name, "[1,64]")
print("OUTPUT:", output_name, "[1,64]")
print("IR VERSION:", diagnostic.ir_version)
print("OPSET:", 17)
