from pathlib import Path
import onnx
from onnx import helper, TensorProto, numpy_helper
import numpy as np

ROOT = Path(r"E:\EdgeResilience")

src = ROOT / "experiments" / "v4_output_head_diagnostic.onnx"
dst = ROOT / "experiments" / "v4_output_head_tanh_diagnostic.onnx"

model = onnx.load(str(src))
init = {x.name: x for x in model.graph.initializer}

w_ln = numpy_helper.to_array(init["output_head.0.weight"]).astype(np.float32)
b_ln = numpy_helper.to_array(init["output_head.0.bias"]).astype(np.float32)

w1 = numpy_helper.to_array(init["output_head.1.weight"]).astype(np.float32)
b1 = numpy_helper.to_array(init["output_head.1.bias"]).astype(np.float32)

w2 = numpy_helper.to_array(init["output_head.4.weight"]).astype(np.float32)
b2 = numpy_helper.to_array(init["output_head.4.bias"]).astype(np.float32)

input_name = "/ReduceSum_output_0"
output_name = "future_resilience_degradation"

x = helper.make_tensor_value_info(
    input_name,
    TensorProto.FLOAT,
    [1, 64],
)

y = helper.make_tensor_value_info(
    output_name,
    TensorProto.FLOAT,
    [1],
)

nodes = [
    helper.make_node(
        "LayerNormalization",
        [input_name, "ln_weight", "ln_bias"],
        ["ln_out"],
        name="LayerNorm",
        axis=-1,
        epsilon=1e-5,
    ),

    # FC1: [1,64] x [32,64]^T -> [1,32]
    helper.make_node(
        "Gemm",
        ["ln_out", "fc1_weight", "fc1_bias"],
        ["fc1_out"],
        name="FC1",
        transB=1,
    ),

    # tanh-GELU:
    # 0.5*x*(1+tanh(sqrt(2/pi)*(x+0.044715*x^3)))

    helper.make_node(
        "Mul",
        ["fc1_out", "fc1_out"],
        ["x2"],
        name="Square",
    ),

    helper.make_node(
        "Mul",
        ["x2", "fc1_out"],
        ["x3"],
        name="Cube",
    ),

    helper.make_node(
        "Mul",
        ["x3", "gelu_coeff"],
        ["scaled_x3"],
        name="GELU_Cubic",
    ),

    helper.make_node(
        "Add",
        ["fc1_out", "scaled_x3"],
        ["gelu_inner"],
        name="GELU_Add",
    ),

    helper.make_node(
        "Mul",
        ["gelu_inner", "sqrt_2_over_pi"],
        ["gelu_scaled"],
        name="GELU_Scale",
    ),

    helper.make_node(
        "Tanh",
        ["gelu_scaled"],
        ["gelu_tanh"],
        name="GELU_Tanh",
    ),

    helper.make_node(
        "Add",
        ["gelu_tanh", "one"],
        ["gelu_plus_one"],
        name="GELU_PlusOne",
    ),

    helper.make_node(
        "Mul",
        ["fc1_out", "gelu_plus_one"],
        ["gelu_product"],
        name="GELU_Product",
    ),

    helper.make_node(
        "Mul",
        ["gelu_product", "half"],
        ["gelu_out"],
        name="GELU_Half",
    ),

    # FC2: [1,32] x [1,32]^T -> [1,1]
    helper.make_node(
        "Gemm",
        ["gelu_out", "fc2_weight", "fc2_bias"],
        ["fc2_out"],
        name="FC2",
        transB=1,
    ),

    helper.make_node(
        "Sigmoid",
        ["fc2_out"],
        ["sigmoid_out"],
        name="Sigmoid",
    ),

    helper.make_node(
        "Reshape",
        ["sigmoid_out", "output_shape"],
        [output_name],
        name="Reshape",
    ),
]

constants = [
    numpy_helper.from_array(w_ln, "ln_weight"),
    numpy_helper.from_array(b_ln, "ln_bias"),

    numpy_helper.from_array(w1, "fc1_weight"),
    numpy_helper.from_array(b1, "fc1_bias"),

    numpy_helper.from_array(w2, "fc2_weight"),
    numpy_helper.from_array(b2, "fc2_bias"),

    numpy_helper.from_array(
        np.array(0.044715, dtype=np.float32),
        "gelu_coeff",
    ),

    numpy_helper.from_array(
        np.array(np.sqrt(2.0 / np.pi), dtype=np.float32),
        "sqrt_2_over_pi",
    ),

    numpy_helper.from_array(
        np.array(1.0, dtype=np.float32),
        "one",
    ),

    numpy_helper.from_array(
        np.array(0.5, dtype=np.float32),
        "half",
    ),

    numpy_helper.from_array(
        np.array([1], dtype=np.int64),
        "output_shape",
    ),
]

graph = helper.make_graph(
    nodes,
    "EdgeResilience_V4_OutputHead_TanhGELU_Diagnostic",
    [x],
    [y],
    initializer=constants,
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
