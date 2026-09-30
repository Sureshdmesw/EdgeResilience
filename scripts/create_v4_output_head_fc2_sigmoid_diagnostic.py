from pathlib import Path
import onnx
from onnx import shape_inference

ROOT = Path(r"E:\EdgeResilience")

src = ROOT / "experiments" / "v4_output_head_diagnostic.onnx"
dst = ROOT / "experiments" / "v4_output_head_fc2_sigmoid_diagnostic.onnx"

model = onnx.load(str(src))
model = shape_inference.infer_shapes(model)

# Start from GELU output and retain:
# FC2 Gemm -> Sigmoid -> Squeeze
start_name = "/output_head/output_head.2/Mul_1_output_0"

nodes = []
started = False

for node in model.graph.node:
    if start_name in node.input:
        started = True

    if started:
        nodes.append(node)

print("Selected nodes:")
for n in nodes:
    print(" ", n.op_type, n.name)

if not nodes:
    raise RuntimeError("Could not locate FC2/Sigmoid path")

final_output = nodes[-1].output[0]

value_info = None

for vi in list(model.graph.value_info) + list(model.graph.output):
    if vi.name == final_output:
        value_info = vi
        break

if value_info is None:
    raise RuntimeError(
        f"Could not find shape information for {final_output}"
    )

# Find the GELU output tensor's shape/type
gelu_info = None

for vi in list(model.graph.value_info) + list(model.graph.input):
    if vi.name == start_name:
        gelu_info = vi
        break

if gelu_info is None:
    raise RuntimeError(
        f"Could not find GELU input information for {start_name}"
    )

new_graph = onnx.helper.make_graph(
    nodes=nodes,
    name="V4_OutputHead_FC2_Sigmoid_Diagnostic",
    inputs=[gelu_info],
    outputs=[value_info],
    initializer=list(model.graph.initializer),
)

new_model = onnx.helper.make_model(
    new_graph,
    producer_name="EdgeResilience",
)

new_model.ir_version = 10

del new_model.opset_import[:]

for opset in model.opset_import:
    imp = new_model.opset_import.add()
    imp.domain = opset.domain
    imp.version = opset.version

onnx.checker.check_model(new_model)
onnx.save(new_model, str(dst))

print()
print("FC2 + SIGMOID DIAGNOSTIC CREATED")
print("OUTPUT:", dst)
print("FINAL OUTPUT:", final_output)
print("NODES:", len(nodes))
print("FILE EXISTS:", dst.exists())
print("FILE SIZE:", dst.stat().st_size if dst.exists() else 0)
