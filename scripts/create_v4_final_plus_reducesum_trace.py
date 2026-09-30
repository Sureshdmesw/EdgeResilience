from pathlib import Path
import onnx

ROOT = Path(r"E:\EdgeResilience")

src = ROOT / "models" / "edgeresilience" / "snapdragon" / "temporal_predictor_v4_qnn_ready.onnx"
out = ROOT / "experiments" / "v4_final_plus_reducesum_trace.onnx"

targets = [
    "/ReduceSum_output_0",
    "future_resilience_degradation",
]

model = onnx.load(str(src))
model = onnx.shape_inference.infer_shapes(model)

available = {}

for v in model.graph.value_info:
    available[v.name] = v

for v in model.graph.input:
    available[v.name] = v

for v in model.graph.output:
    available[v.name] = v

for name in targets:
    if name not in available:
        raise RuntimeError(f"Missing tensor: {name}")

    print("FOUND:", name)

new_outputs = []

for name in targets:
    v = available[name]

    shape = []

    for d in v.type.tensor_type.shape.dim:
        if d.HasField("dim_value"):
            shape.append(d.dim_value)
        else:
            shape.append(None)

    new_outputs.append(
        onnx.helper.make_tensor_value_info(
            name,
            v.type.tensor_type.elem_type,
            shape
        )
    )

del model.graph.output[:]
model.graph.output.extend(new_outputs)

# Remove promoted tensors from value_info to satisfy ONNX IR.
target_set = set(targets)

remaining = [
    v for v in model.graph.value_info
    if v.name not in target_set
]

del model.graph.value_info[:]
model.graph.value_info.extend(remaining)

onnx.checker.check_model(model)
onnx.save(model, str(out))

# Reload validation.
check = onnx.load(str(out))
onnx.checker.check_model(check)

print()
print("MODEL:", out)
print("SIZE:", out.stat().st_size)

print()
print("OUTPUTS:")
for o in check.graph.output:
    print(" ", o.name)

print()
print("ONNX CHECKER: PASS")
