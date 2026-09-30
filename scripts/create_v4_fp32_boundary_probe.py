import onnx
from onnx import helper, TensorProto
from pathlib import Path

src = Path(r"models\edgeresilience\snapdragon\temporal_predictor_v4_qnn_ready.onnx")
dst = Path(r"experiments\v4_fp32_boundary_probe.onnx")

m = onnx.load(src)

# Locate the ReduceSum that feeds the output head.
target = None
for n in m.graph.node:
    if n.op_type == "ReduceSum":
        target = n
        break

if target is None:
    raise RuntimeError("ReduceSum node not found")

print("ReduceSum node:", target.name)
print("ReduceSum output:", target.output[0])

# Preserve the production graph exactly, but expose the
# transformer -> output-head boundary as an additional FP32 output.
boundary = target.output[0]

existing = {o.name for o in m.graph.output}
if boundary not in existing:
    vi = helper.make_tensor_value_info(
        boundary,
        TensorProto.FLOAT,
        [1, 64],
    )
    m.graph.output.append(vi)

onnx.checker.check_model(m)
onnx.save(m, dst)

print("Created:", dst)
print("Outputs:")
for o in m.graph.output:
    print(" ", o.name)
