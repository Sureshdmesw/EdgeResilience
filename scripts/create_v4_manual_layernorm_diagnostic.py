from pathlib import Path
import onnx
from onnx import helper, TensorProto, numpy_helper
import numpy as np

ROOT = Path(r"E:\EdgeResilience")

src = ROOT / "experiments" / "v4_layernorm_diagnostic.onnx"
dst = ROOT / "experiments" / "v4_manual_layernorm_diagnostic.onnx"

model = onnx.load(str(src))
init = {x.name: x for x in model.graph.initializer}

w = numpy_helper.to_array(init["ln_weight"]).astype(np.float32)
b = numpy_helper.to_array(init["ln_bias"]).astype(np.float32)

input_name = "/ReduceSum_output_0"
output_name = "layernorm_output"

x_info = helper.make_tensor_value_info(
    input_name,
    TensorProto.FLOAT,
    [1, 64],
)

y_info = helper.make_tensor_value_info(
    output_name,
    TensorProto.FLOAT,
    [1, 64],
)

nodes = [
    # mean over last dimension
    helper.make_node(
        "ReduceMean",
        [input_name],
        ["mean"],
        name="ReduceMean",
        axes=[1],
        keepdims=1,
    ),

    # x - mean
    helper.make_node(
        "Sub",
        [input_name, "mean"],
        ["centered"],
        name="SubtractMean",
    ),

    # (x - mean)^2
    helper.make_node(
        "Mul",
        ["centered", "centered"],
        ["squared"],
        name="Square",
    ),

    # variance
    helper.make_node(
        "ReduceMean",
        ["squared"],
        ["variance"],
        name="ReduceVariance",
        axes=[1],
        keepdims=1,
    ),

    # variance + epsilon
    helper.make_node(
        "Add",
        ["variance", "epsilon"],
        ["variance_eps"],
        name="AddEpsilon",
    ),

    # sqrt(variance + epsilon)
    helper.make_node(
        "Sqrt",
        ["variance_eps"],
        ["std"],
        name="Sqrt",
    ),

    # normalized
    helper.make_node(
        "Div",
        ["centered", "std"],
        ["normalized"],
        name="Divide",
    ),

    # affine scale
    helper.make_node(
        "Mul",
        ["normalized", "ln_weight"],
        ["scaled"],
        name="Scale",
    ),

    # affine bias
    helper.make_node(
        "Add",
        ["scaled", "ln_bias"],
        [output_name],
        name="Bias",
    ),
]

initializers = [
    numpy_helper.from_array(w, "ln_weight"),
    numpy_helper.from_array(b, "ln_bias"),
    numpy_helper.from_array(
        np.array(1e-5, dtype=np.float32),
        "epsilon",
    ),
]

graph = helper.make_graph(
    nodes,
    "EdgeResilience_V4_Manual_LayerNorm_Diagnostic",
    [x_info],
    [y_info],
    initializer=initializers,
)

diagnostic = helper.make_model(
    graph,
    producer_name="EdgeResilience",
    opset_imports=[
        helper.make_opsetid("", 17)
    ],
)

diagnostic.ir_version = 10

onnx.checker.check_model(diagnostic)
onnx.save(diagnostic, str(dst))

print("CREATED:", dst)
print("NODES:", len(nodes))
print("IR VERSION:", diagnostic.ir_version)
print("OPSET:", 17)
