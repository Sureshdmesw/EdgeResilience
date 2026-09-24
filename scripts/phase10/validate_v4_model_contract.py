from pathlib import Path
import json
import onnx

MODEL = Path(
    r"E:\EdgeResilience\models\edgeresilience\snapdragon\v4_temporal_pooling_plus_head_qnn_control_clean.onnx"
)

OUT = Path(
    r"E:\EdgeResilience\artifacts\phase10\reference_inference\v4_model_contract.json"
)

model = onnx.load(MODEL)
onnx.checker.check_model(model)

def shape(tensor):
    return [
        d.dim_value if d.dim_value else d.dim_param
        for d in tensor.type.tensor_type.shape.dim
    ]

data = {
    "model": str(MODEL),
    "onnx_checker": "PASSED",
    "inputs": [
        {
            "name": x.name,
            "shape": shape(x),
            "element_type": x.type.tensor_type.elem_type,
        }
        for x in model.graph.input
    ],
    "outputs": [
        {
            "name": x.name,
            "shape": shape(x),
            "element_type": x.type.tensor_type.elem_type,
        }
        for x in model.graph.output
    ],
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(data, indent=2))

print("=" * 70)
print("PHASE 10 MODEL CONTRACT VALIDATION")
print("=" * 70)
print("Model:", MODEL)
print("ONNX checker: PASSED")

for x in data["inputs"]:
    print("INPUT :", x)

for x in data["outputs"]:
    print("OUTPUT:", x)

print("Evidence:", OUT)
