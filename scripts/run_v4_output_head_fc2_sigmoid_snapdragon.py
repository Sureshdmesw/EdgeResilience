from pathlib import Path
import numpy as np
import qai_hub as hub

ROOT = Path(r"E:\EdgeResilience")

input_file = ROOT / "experiments" / "v4_output_head_gelu_cpu_output.npy"
cpu_file = ROOT / "experiments" / "v4_output_head_fc2_sigmoid_cpu_output.npy"
snap_file = ROOT / "experiments" / "v4_output_head_fc2_sigmoid_snapdragon_output.npy"

x = np.load(input_file).astype(np.float32)
cpu = np.load(cpu_file).astype(np.float32)

compile_job = hub.get_job("jp4yzr4lp")
target = compile_job.get_target_model()

print("TARGET MODEL:", target)
print("TARGET MODEL ID:", target.model_id)
print("INPUT SHAPE:", x.shape)
print("INPUT FIRST 8:", x.reshape(-1)[:8])

inputs = {
    "/output_head/output_head.2/Mul_1_output_0": [x]
}

job = hub.submit_inference_job(
    model=target,
    device=hub.Device("Snapdragon X Elite CRD"),
    inputs=inputs,
    name="EdgeResilience V4 FC2 Sigmoid Diagnostic Inference"
)

print("INFERENCE JOB:", job.job_id)

job.wait()

print("INFERENCE COMPLETE")

outputs = job.download_output_data()

print("OUTPUT KEYS:", list(outputs.keys()))

snap = np.asarray(outputs["output_0"][0], dtype=np.float32)

np.save(snap_file, snap)

abs_err = np.abs(cpu - snap)

max_abs = float(np.max(abs_err))
mean_abs = float(np.mean(abs_err))
rmse = float(np.sqrt(np.mean((cpu - snap) ** 2)))

print()
print("=== FC2 + SIGMOID CPU vs SNAPDRAGON ===")
print("CPU output:", cpu)
print("Snapdragon output:", snap)
print()
print("CPU value:", float(cpu.reshape(-1)[0]))
print("Snapdragon value:", float(snap.reshape(-1)[0]))
print("Absolute error:", max_abs)
print("Mean absolute error:", mean_abs)
print("RMSE:", rmse)
print()
print("SAVED:", snap_file)
