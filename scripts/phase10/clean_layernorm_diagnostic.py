import onnx
from pathlib import Path

src = Path(r"E:\EdgeResilience\models\edgeresilience\snapdragon\v4_diag_layernorm1.onnx")
dst = Path(r"E:\EdgeResilience\models\edgeresilience\snapdragon\v4_diag_layernorm1_clean.onnx")

m = onnx.load(src)

target = "layer_norm_3"

# Remove target from value_info because it is now graph output.
kept = [v for v in m.graph.value_info if v.name != target]

del m.graph.value_info[:]
m.graph.value_info.extend(kept)

onnx.checker.check_model(m)
onnx.save(m, dst)

print("Created:", dst)
print("Output:", m.graph.output[0].name)
print("Remaining duplicate:",
      [v.name for v in m.graph.value_info
       if v.name in {o.name for o in m.graph.output}])
print("ONNX CHECKER: PASS")
