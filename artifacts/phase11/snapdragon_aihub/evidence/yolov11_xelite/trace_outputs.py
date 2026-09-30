import onnx

path = r"artifacts\phase11\snapdragon_aihub\compile\yolov11_xelite\extracted\job_j5wlly94p_optimized_onnx\model.onnx"
m = onnx.load(path)

producers = {}
for n in m.graph.node:
    for out in n.output:
        producers[out] = n

def trace(tensor, depth=0, seen=None):
    if seen is None:
        seen = set()

    if tensor in seen or depth > 25:
        return

    seen.add(tensor)
    n = producers.get(tensor)

    if n is None:
        print("  " * depth + f"INPUT/TENSOR: {tensor}")
        return

    print("  " * depth + f"{n.name} [{n.op_type}]")
    print("  " * depth + f"  output: {tensor}")

    for inp in n.input:
        trace(inp, depth + 1, seen)

print("=== SCORE PATH: output_1 ===")
trace("output_1")

print("\n=== CLASS PATH: output_2 ===")
trace("output_2")
