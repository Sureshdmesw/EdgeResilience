from pathlib import Path
import onnx
from onnx import shape_inference

ROOT = Path(r"E:\EdgeResilience")

src = ROOT / "experiments" / "v4_output_head_diagnostic.onnx"
dst = ROOT / "experiments" / "v4_output_head_gelu_diagnostic.onnx"

model = onnx.load(str(src))
model = shape_inference.infer_shapes(model)

nodes = []

gemm_count = 0

for node in model.graph.node:
    nodes.append(node)

    if node.op_type == "Gemm":
        gemm_count += 1

        # Stop after GELU, immediately after FC1.
        if gemm_count == 1:
            continue

    # GELU ends at Mul_1
    if node.name.endswith("output_head.2/Mul_1"):
        break

print("Selected nodes:")
for n in nodes:
    print(" ", n.op_type, n.name)

gelu_node = nodes[-1]
gelu_output = gelu_node.output[0]

value_info = None

for vi in list(model.graph.value_info) + list(model.graph.output):
    if vi.name == gelu_output:
        value_info = vi
        break

if value_info is None:
    raise RuntimeError(
        f"Could not find shape information for {gelu_output}"
    )

new_graph = onnx.helper.make_graph(
    nodes=nodes,
    name="V4_OutputHead_GELU_Diagnostic",
    inputs=list(model.graph.input),
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
print("GELU DIAGNOSTIC CREATED")
print("OUTPUT:", dst)
print("GELU OUTPUT:", gelu_output)
print("NODES:", len(nodes))
print("FILE EXISTS:", dst.exists())
print("FILE SIZE:", dst.stat().st_size if dst.exists() else 0)
