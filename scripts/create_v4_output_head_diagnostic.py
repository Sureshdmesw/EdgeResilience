from pathlib import Path
import onnx
from onnx import helper, TensorProto

ROOT = Path(r"E:\EdgeResilience")

src = ROOT / "models" / "edgeresilience" / "snapdragon" / "temporal_predictor_v4_qnn_ready.onnx"
dst = ROOT / "experiments" / "v4_output_head_diagnostic.onnx"

model = onnx.load(str(src))
model = onnx.shape_inference.infer_shapes(model)

start_tensor = "/ReduceSum_output_0"
end_tensor = "future_resilience_degradation"

# Find the first node AFTER ReduceSum.
reduce_index = next(
    i for i, n in enumerate(model.graph.node)
    if start_tensor in n.output
)

end_index = next(
    i for i, n in enumerate(model.graph.node)
    if end_tensor in n.output
)

nodes = list(model.graph.node[reduce_index + 1:end_index + 1])

initializer_names = {x.name for x in model.graph.initializer}

required_initializers = set()

for node in nodes:
    for inp in node.input:
        if inp in initializer_names:
            required_initializers.add(inp)

initializers = [
    x for x in model.graph.initializer
    if x.name in required_initializers
]

input_info = helper.make_tensor_value_info(
    start_tensor,
    TensorProto.FLOAT,
    [1, 64],
)

output_info = helper.make_tensor_value_info(
    end_tensor,
    TensorProto.FLOAT,
    [1],
)

graph = helper.make_graph(
    nodes,
    "EdgeResilience_V4_OutputHead_Diagnostic",
    [input_info],
    [output_info],
    initializer=initializers,
)

diagnostic = helper.make_model(
    graph,
    producer_name="EdgeResilience",
    opset_imports=model.opset_import,
)

onnx.checker.check_model(diagnostic)
onnx.save(diagnostic, str(dst))

print("CREATED:", dst)
print("NODES:", len(nodes))
print("INPUT :", start_tensor, "[1,64]")
print("OUTPUT:", end_tensor, "[1]")
print("INITIALIZERS:", len(initializers))
print()
print("NODE LIST:")
for n in nodes:
    print(n.name, n.op_type, "->", list(n.output))
