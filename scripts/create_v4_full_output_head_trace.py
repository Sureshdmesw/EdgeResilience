from pathlib import Path
import onnx

ROOT = Path(r"E:\EdgeResilience")

src = ROOT / "models" / "edgeresilience" / "snapdragon" / "temporal_predictor_v4_qnn_ready.onnx"
out = ROOT / "experiments" / "v4_full_output_head_trace.onnx"

targets = [
    "/ReduceSum_output_0",
    "/output_head/output_head.0/LayerNormalization_output_0",
    "/output_head/output_head.1/Gemm_output_0",
    "/output_head/output_head.2/Mul_1_output_0",
    "/output_head/output_head.4/Gemm_output_0",
    "future_resilience_degradation",
]

model = onnx.load(str(src))

# Shape inference first.
model = onnx.shape_inference.infer_shapes(model)

# Collect resolved tensor metadata.
available = {}

for v in model.graph.value_info:
    available[v.name] = v

for v in model.graph.input:
    available[v.name] = v

for v in model.graph.output:
    available[v.name] = v

print("TARGET VALIDATION:")
for name in targets:
    print(
        f"  {name}:",
        "FOUND" if name in available else "MISSING"
    )

    if name not in available:
        raise RuntimeError(f"Missing tensor: {name}")

# Create independent output ValueInfo objects.
new_outputs = []

for name in targets:
    original = available[name]

    new_output = onnx.helper.make_tensor_value_info(
        name,
        original.type.tensor_type.elem_type,
        [
            d.dim_value if d.HasField("dim_value") else None
            for d in original.type.tensor_type.shape.dim
        ]
    )

    new_outputs.append(new_output)

# Remove old graph outputs.
del model.graph.output[:]

# Install requested outputs.
model.graph.output.extend(new_outputs)

# IMPORTANT:
# Remove graph value_info entries that are now graph outputs.
remaining_value_info = [
    v for v in model.graph.value_info
    if v.name not in set(targets)
]

del model.graph.value_info[:]
model.graph.value_info.extend(remaining_value_info)

# Validate.
onnx.checker.check_model(model)

onnx.save(model, str(out))

# Reload and validate again.
check = onnx.load(str(out))
onnx.checker.check_model(check)

print()
print("TRACE MODEL CREATED:", out)
print("SIZE:", out.stat().st_size)

print()
print("GRAPH OUTPUTS:")
for output in check.graph.output:
    dims = []

    for d in output.type.tensor_type.shape.dim:
        if d.HasField("dim_value"):
            dims.append(d.dim_value)
        else:
            dims.append("?")

    print(" ", output.name, dims)

print()
print("VALUE_INFO / OUTPUT COLLISIONS:")

output_names = {o.name for o in check.graph.output}

collisions = [
    v.name
    for v in check.graph.value_info
    if v.name in output_names
]

print(collisions)

if collisions:
    raise RuntimeError(
        "Trace model still contains value_info/output collisions"
    )

print()
print("ONNX CHECKER: PASS")
print("TRACE MODEL READY")
