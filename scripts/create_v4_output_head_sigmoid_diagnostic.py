from pathlib import Path
import hashlib
import json
import numpy as np
import onnx
from onnx import helper, TensorProto

ROOT = Path(r"E:\EdgeResilience")

cpu_fc2_file = ROOT / "experiments" / "v4_output_head_fc2_cpu_output.npy"
model_file = ROOT / "experiments" / "v4_output_head_sigmoid_diagnostic.onnx"
cpu_output_file = ROOT / "experiments" / "v4_output_head_sigmoid_cpu_output.npy"

# Exact CPU FC2 output
x = np.load(cpu_fc2_file).astype(np.float32).reshape(1, 1)

print("CPU FC2 INPUT:", x)
print("INPUT SHAPE:", x.shape)
print("INPUT SHA256:", hashlib.sha256(cpu_fc2_file.read_bytes()).hexdigest())

input_name = "fc2_output"
output_name = "future_resilience_degradation"

input_tensor = helper.make_tensor_value_info(
    input_name,
    TensorProto.FLOAT,
    [1, 1]
)

output_tensor = helper.make_tensor_value_info(
    output_name,
    TensorProto.FLOAT,
    [1, 1]
)

sigmoid_node = helper.make_node(
    "Sigmoid",
    inputs=[input_name],
    outputs=[output_name],
    name="output_head_sigmoid"
)

graph = helper.make_graph(
    [sigmoid_node],
    "V4_Sigmoid_Diagnostic",
    [input_tensor],
    [output_tensor]
)

model = helper.make_model(
    graph,
    producer_name="EdgeResilience",
    ir_version=10,
    opset_imports=[helper.make_opsetid("", 17)]
)

onnx.checker.check_model(model)

onnx.save(model, model_file)

print()
print("MODEL CREATED:", model_file)
print("SIZE:", model_file.stat().st_size)

# CPU reference
import onnxruntime as ort

session = ort.InferenceSession(
    str(model_file),
    providers=["CPUExecutionProvider"]
)

result = session.run(
    [output_name],
    {input_name: x}
)[0]

np.save(cpu_output_file, result.astype(np.float32))

print()
print("CPU SIGMOID OUTPUT:", result)
print("CPU SIGMOID SCALAR:", float(result.reshape(-1)[0]))
print("CPU OUTPUT SAVED:", cpu_output_file)
