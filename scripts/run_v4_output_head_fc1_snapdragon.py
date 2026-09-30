from pathlib import Path
import numpy as np
import qai_hub as hub

ROOT = Path(r"E:\EdgeResilience")

input_file = ROOT / "experiments" / "v4_output_head_control_input.npy"
cpu_file = ROOT / "experiments" / "v4_output_head_fc1_cpu_output.npy"
snap_file = ROOT / "experiments" / "v4_output_head_fc1_snapdragon_output.npy"

x = np.load(input_file).astype(np.float32)
cpu = np.load(cpu_file).astype(np.float32)

compile_job = hub.get_job("j5m0jxoyg")
target = compile_job.get_target_model()

print("TARGET MODEL:", target)
print("TARGET MODEL ID:", target.model_id)
print("INPUT SHAPE:", x.shape)

inputs = {
    "/ReduceSum_output_0": [x]
}

job = hub.submit_inference_job(
    model=target,
    device=hub.Device("Snapdragon X Elite CRD"),
    inputs=inputs,
    name="EdgeResilience V4 FC1 Diagnostic Inference"
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
print("=== FC1 CPU vs SNAPDRAGON ===")
print("CPU shape:", cpu.shape)
print("Snapdragon shape:", snap.shape)
print()
print("CPU first 8:")
print(cpu.reshape(-1)[:8])
print()
print("Snapdragon first 8:")
print(snap.reshape(-1)[:8])
print()
print("Max absolute error:", max_abs)
print("Mean absolute error:", mean_abs)
print("RMSE:", rmse)
print()
print("CPU min/max:", float(cpu.min()), float(cpu.max()))
print("Snapdragon min/max:", float(snap.min()), float(snap.max()))
print("Snapdragon mean:", float(snap.mean()))
print("Snapdragon std:", float(snap.std()))
print()
print("SAVED:", snap_file)
