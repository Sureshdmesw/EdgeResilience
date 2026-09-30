from pathlib import Path
import numpy as np
import onnx
from onnx import helper, TensorProto, numpy_helper

ROOT = Path(r"E:\EdgeResilience")

src = ROOT / "models" / "edgeresilience" / "snapdragon" / "temporal_predictor_v4_qnn_ready.onnx"
out = ROOT / "experiments" / "v4_reducesum_boundary_diagnostic.onnx"

print("SOURCE:", src)
print("EXISTS:", src.exists())

model = onnx.load(str(src))

# Locate the ReduceSum node producing the output-head input
target_node = None

for node in model.graph.node:
    if node.op_type == "ReduceSum":
        target_node = node
        break

if target_node is None:
    raise RuntimeError("ReduceSum node not found")

print("FOUND NODE:", target_node.name)
print("INPUTS:", list(target_node.input))
print("OUTPUTS:", list(target_node.output))

target_output = target_node.output[0]

# Infer shapes
inferred = onnx.shape_inference.infer_shapes(model)

value_info = {}

for v in inferred.graph.value_info:
    value_info[v.name] = v

for v in inferred.graph.input:
    value_info[v.name] = v

for v in inferred.graph.output:
    value_info[v.name] = v

if target_output not in value_info:
    raise RuntimeError(
        f"Shape information not found for {target_output}"
    )

target_vi = value_info[target_output]

print(
    "TARGET TYPE:",
    target_vi.type.tensor_type.elem_type
)

dims = []

for d in target_vi.type.tensor_type.shape.dim:
    if d.HasField("dim_value"):
        dims.append(d.dim_value)
    else:
        dims.append(None)

print("TARGET SHAPE:", dims)

# Promote the ReduceSum output to a graph output.
new_output = helper.make_tensor_value_info(
    target_output,
    TensorProto.FLOAT,
    dims
)

# Keep original graph input(s)
new_inputs = list(model.graph.input)

# Keep original nodes, but expose ReduceSum output.
new_outputs = [new_output]

diagnostic_graph = helper.make_graph(
    list(model.graph.node),
    "V4_ReduceSum_Boundary_Diagnostic",
    new_inputs,
    new_outputs,
    initializer=list(model.graph.initializer),
)

diagnostic_model = helper.make_model(
    diagnostic_graph,
    producer_name="EdgeResilience",
    ir_version=model.ir_version,
    opset_imports=list(model.opset_import),
)

onnx.checker.check_model(diagnostic_model)
onnx.save(diagnostic_model, str(out))

print()
print("DIAGNOSTIC CREATED:", out)
print("SIZE:", out.stat().st_size)
print("OUTPUT:", target_output)
print("SUCCESS")
