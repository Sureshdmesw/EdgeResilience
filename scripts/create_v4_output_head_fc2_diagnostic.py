from pathlib import Path
import onnx
from onnx import shape_inference

ROOT = Path(r"E:\EdgeResilience")

src = ROOT / "experiments" / "v4_output_head_diagnostic.onnx"
dst = ROOT / "experiments" / "v4_output_head_fc2_diagnostic.onnx"

model = onnx.load(str(src))
model = shape_inference.infer_shapes(model)

start_name = "/output_head/output_head.2/Mul_1_output_0"

nodes = []
started = False

for node in model.graph.node:
    if start_name in node.input:
        started = True

    if started:
        nodes.append(node)

        # Stop immediately after FC2 Gemm
        if node.op_type == "Gemm":
            break

print("Selected nodes:")
for n in nodes:
    print(" ", n.op_type, n.name)

if len(nodes) != 1 or nodes[0].op_type != "Gemm":
    raise RuntimeError(
        f"Expected exactly one FC2 Gemm, got {len(nodes)} nodes"
    )

fc2_node = nodes[0]
fc2_output = fc2_node.output[0]

# Shape/type information for input
input_info = None

for vi in list(model.graph.value_info) + list(model.graph.input):
    if vi.name == start_name:
        input_info = vi
        break

if input_info is None:
    raise RuntimeError(f"Missing input info: {start_name}")

# Shape/type information for output
output_info = None

for vi in list(model.graph.value_info) + list(model.graph.output):
    if vi.name == fc2_output:
        output_info = vi
        break

if output_info is None:
    raise RuntimeError(f"Missing output info: {fc2_output}")

new_graph = onnx.helper.make_graph(
    nodes=nodes,
    name="V4_OutputHead_FC2_Diagnostic",
    inputs=[input_info],
    outputs=[output_info],
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
print("FC2 DIAGNOSTIC CREATED")
print("OUTPUT:", dst)
print("INPUT:", start_name)
print("FC2 OUTPUT:", fc2_output)
print("NODES:", len(nodes))
print("FILE EXISTS:", dst.exists())
print("FILE SIZE:", dst.stat().st_size if dst.exists() else 0)
