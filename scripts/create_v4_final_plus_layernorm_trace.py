from pathlib import Path
import onnx
from onnx import shape_inference

ROOT = Path(r"E:\EdgeResilience")

src = ROOT / "models" / "edgeresilience" / "snapdragon" / "temporal_predictor_v4_qnn_ready.onnx"
dst = ROOT / "experiments" / "v4_final_plus_layernorm_trace.onnx"

print("SOURCE:", src)

model = onnx.load(src)

# Infer shapes so internal tensors have complete type/shape information.
model = shape_inference.infer_shapes(model)

wanted = [
    "/output_head/output_head.0/LayerNormalization_output_0",
    "future_resilience_degradation",
]

# Build a lookup across all known tensor metadata.
tensor_info = {}

for vi in model.graph.input:
    tensor_info[vi.name] = vi

for vi in model.graph.value_info:
    tensor_info[vi.name] = vi

for vi in model.graph.output:
    tensor_info[vi.name] = vi

# Preserve only the final production output.
final_outputs = [
    o for o in model.graph.output
    if o.name == "future_resilience_degradation"
]

if len(final_outputs) != 1:
    raise RuntimeError("Could not find production output")

# Locate LayerNorm tensor metadata.
layernorm_name = wanted[0]

if layernorm_name not in tensor_info:
    raise RuntimeError(
        f"LayerNorm tensor metadata not found: {layernorm_name}"
    )

layernorm_vi = tensor_info[layernorm_name]

# Replace graph outputs.
del model.graph.output[:]

# First: LayerNorm diagnostic output.
model.graph.output.append(layernorm_vi)

# Second: unchanged production final output.
model.graph.output.append(final_outputs[0])

onnx.checker.check_model(model)
onnx.save(model, dst)

print()
print("CREATED:", dst)
print("SIZE:", dst.stat().st_size)

print()
print("OUTPUTS:")
for o in model.graph.output:
    tensor_type = o.type.tensor_type
    dims = []

    for d in tensor_type.shape.dim:
        if d.HasField("dim_value"):
            dims.append(d.dim_value)
        elif d.HasField("dim_param"):
            dims.append(d.dim_param)
        else:
            dims.append("?")

    print(f"  {o.name}")
    print(f"    dtype: {tensor_type.elem_type}")
    print(f"    shape: {dims}")

print()
print("ONNX CHECKER: PASS")
