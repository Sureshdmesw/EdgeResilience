import onnx
from onnx import helper, TensorProto, numpy_helper
import numpy as np

X = helper.make_tensor_value_info(
    "x", TensorProto.FLOAT, [12, 1, 192]
)

Yq = helper.make_tensor_value_info(
    "q", TensorProto.FLOAT, [4, 12, 16]
)

Yk = helper.make_tensor_value_info(
    "k", TensorProto.FLOAT, [4, 12, 16]
)

Yv = helper.make_tensor_value_info(
    "v", TensorProto.FLOAT, [4, 12, 16]
)

shape_view = numpy_helper.from_array(
    np.array([12, 1, 3, 64], dtype=np.int64),
    name="shape_view"
)

axes_unsqueeze = numpy_helper.from_array(
    np.array([0], dtype=np.int64),
    name="axes_unsqueeze"
)

axes_squeeze = numpy_helper.from_array(
    np.array([2], dtype=np.int64),
    name="axes_squeeze"
)

shape_head = numpy_helper.from_array(
    np.array([12, 4, 16], dtype=np.int64),
    name="shape_head"
)

idx0 = numpy_helper.from_array(
    np.array(0, dtype=np.int64),
    name="idx0"
)

idx1 = numpy_helper.from_array(
    np.array(1, dtype=np.int64),
    name="idx1"
)

idx2 = numpy_helper.from_array(
    np.array(2, dtype=np.int64),
    name="idx2"
)

nodes = [
    helper.make_node(
        "Reshape",
        ["x", "shape_view"],
        ["view"],
        name="qkv_reshape",
    ),

    helper.make_node(
        "Unsqueeze",
        ["view", "axes_unsqueeze"],
        ["unsqueeze"],
        name="qkv_unsqueeze",
    ),

    # V4 actual exported permutation:
    # [1,12,1,3,64] -> [3,12,1,1,64]
    helper.make_node(
        "Transpose",
        ["unsqueeze"],
        ["transpose"],
        name="qkv_transpose",
        perm=[3, 1, 2, 0, 4],
    ),

    helper.make_node(
        "Squeeze",
        ["transpose", "axes_squeeze"],
        ["squeeze"],
        name="qkv_squeeze",
    ),

    helper.make_node(
        "Gather",
        ["squeeze", "idx0"],
        ["q_select"],
        name="q_gather",
        axis=0,
    ),

    helper.make_node(
        "Gather",
        ["squeeze", "idx1"],
        ["k_select"],
        name="k_gather",
        axis=0,
    ),

    helper.make_node(
        "Gather",
        ["squeeze", "idx2"],
        ["v_select"],
        name="v_gather",
        axis=0,
    ),

    helper.make_node(
        "Reshape",
        ["q_select", "shape_head"],
        ["q_view"],
        name="q_reshape",
    ),

    helper.make_node(
        "Reshape",
        ["k_select", "shape_head"],
        ["k_view"],
        name="k_reshape",
    ),

    helper.make_node(
        "Reshape",
        ["v_select", "shape_head"],
        ["v_view"],
        name="v_reshape",
    ),

    helper.make_node(
        "Transpose",
        ["q_view"],
        ["q"],
        name="q_transpose",
        perm=[1, 0, 2],
    ),

    helper.make_node(
        "Transpose",
        ["k_view"],
        ["k"],
        name="k_transpose",
        perm=[1, 0, 2],
    ),

    helper.make_node(
        "Transpose",
        ["v_view"],
        ["v"],
        name="v_transpose",
        perm=[1, 0, 2],
    ),
]

graph = helper.make_graph(
    nodes,
    "V4QKVStructureControl",
    [X],
    [Yq, Yk, Yv],
    initializer=[
        shape_view,
        axes_unsqueeze,
        axes_squeeze,
        shape_head,
        idx0,
        idx1,
        idx2,
    ],
)

model = helper.make_model(
    graph,
    producer_name="EdgeResilience",
    ir_version=10,
    opset_imports=[helper.make_opsetid("", 17)],
)

onnx.checker.check_model(model, full_check=True)

out = r".\models\edgeresilience\snapdragon\v4_qkv_structure_control.onnx"
onnx.save_model(model, out)

print("created:", out)
print("IR:", model.ir_version)
print("opset:", model.opset_import[0].version)
print("input:", "[12,1,192]")
print("outputs:", "[4,12,16] x 3")
