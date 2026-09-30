import onnx
import onnxruntime as ort
import numpy as np

src = r"artifacts\phase11\snapdragon_aihub\compile\yolov11_xelite\extracted\job_j5wlly94p_optimized_onnx\model.onnx"
dbg = r"artifacts\phase11\snapdragon_aihub\evidence\yolov11_xelite\debug_pre_sigmoid.onnx"

m = onnx.load(src)

sigmoid = next(n for n in m.graph.node if n.name == "node_sigmoid")
pre_sigmoid = sigmoid.input[0]

print("SIGMOID NODE:", sigmoid.name)
print("SIGMOID INPUT:", pre_sigmoid)

producer = next(
    (n for n in m.graph.node if pre_sigmoid in n.output),
    None
)

print(
    "PRE-SIGMOID PRODUCER:",
    producer.name if producer else "GRAPH INPUT/INITIALIZER",
    producer.op_type if producer else ""
)

m.graph.output.append(
    onnx.helper.make_tensor_value_info(
        "pre_sigmoid_debug",
        onnx.TensorProto.FLOAT,
        None
    )
)

# Rename the added output to the actual tensor name.
m.graph.output[-1].name = pre_sigmoid

onnx.save(m, dbg)

print("DEBUG MODEL:", dbg)

sess = ort.InferenceSession(dbg, providers=["CPUExecutionProvider"])

outputs = sess.run(
    None,
    {"image": np.zeros((1, 3, 640, 640), dtype=np.float32)}
)

print("OUTPUT COUNT:", len(outputs))

for i, o in enumerate(outputs):
    print(
        i,
        "shape=", o.shape,
        "dtype=", o.dtype,
        "min=", float(np.min(o)),
        "max=", float(np.max(o)),
        "mean=", float(np.mean(o)),
        "finite=", bool(np.isfinite(o).all())
    )
