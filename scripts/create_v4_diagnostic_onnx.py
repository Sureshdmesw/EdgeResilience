from pathlib import Path
import onnx
from onnx import helper

ROOT = Path(r"E:\EdgeResilience")

src = ROOT / "models" / "edgeresilience" / "snapdragon" / "temporal_predictor_v4_qnn_ready.onnx"
dst = ROOT / "experiments" / "v4_qnn_ready_diagnostic.onnx"

model = onnx.load(str(src))

# Infer missing intermediate tensor shapes
model = onnx.shape_inference.infer_shapes(model)

targets = [
    "/ReduceSum_output_0",
    "/output_head/output_head.0/LayerNormalization_output_0",
    "/output_head/output_head.1/Gemm_output_0",
    "/output_head/output_head.2/Erf_output_0",
    "/output_head/output_head.2/Mul_1_output_0",
    "/output_head/output_head.4/Gemm_output_0",
    "/output_head/output_head.5/Sigmoid_output_0",
    "future_resilience_degradation",
]

existing_outputs = {o.name for o in model.graph.output}

all_values = (
    list(model.graph.value_info)
    + list(model.graph.input)
    + list(model.graph.output)
)

value_map = {v.name: v for v in all_values}

for name in targets:
    if name in existing_outputs:
        continue

    if name not in value_map:
        raise RuntimeError(f"Tensor shape not found: {name}")

    value_info = value_map[name]

    # Clone the ValueInfoProto so we don't mutate the original metadata.
    output_info = onnx.ValueInfoProto()
    output_info.CopyFrom(value_info)

    model.graph.output.append(output_info)

onnx.checker.check_model(model)
onnx.save(model, str(dst))

print("CREATED:", dst)
print("OUTPUTS:")
for o in model.graph.output:
    dims = [
        d.dim_value if d.dim_value else d.dim_param
        for d in o.type.tensor_type.shape.dim
    ]
    print(" ", o.name, dims)
