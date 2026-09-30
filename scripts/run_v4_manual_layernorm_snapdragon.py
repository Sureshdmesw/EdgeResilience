from pathlib import Path
import numpy as np
import qai_hub as hub

ROOT = Path(r"E:\EdgeResilience")

# Exact controlled LayerNorm input
input_file = ROOT / "experiments" / "v4_output_head_control_input.npy"
cpu_file = ROOT / "experiments" / "v4_manual_layernorm_cpu_output.npy"
out_file = ROOT / "experiments" / "v4_manual_layernorm_snapdragon_output.npy"

x = np.load(input_file).astype(np.float32)
cpu = np.load(cpu_file).astype(np.float32)

print("INPUT SHAPE:", x.shape)
print("INPUT DTYPE:", x.dtype)

compile_job = hub.get_job("jp1nrz7ng")
target = compile_job.get_target_model()

print("TARGET MODEL:", target)
print("TARGET MODEL ID:", target.model_id)

inputs = {
    "/ReduceSum_output_0": [x]
}

job = hub.submit_inference_job(
    model=target,
    device=hub.Device("Snapdragon X Elite CRD"),
    inputs=inputs,
    name="EdgeResilience V4 Manual LayerNorm Inference"
)

print("INFERENCE JOB:", job.job_id)

job.wait()

print("INFERENCE COMPLETE")

outputs = job.download_output_data()

print("OUTPUT KEYS:", list(outputs.keys()))

snap = np.asarray(outputs["output_0"][0], dtype=np.float32)

np.save(out_file, snap)

abs_err = np.abs(cpu - snap)

max_abs = float(np.max(abs_err))
mean_abs = float(np.mean(abs_err))
rmse = float(np.sqrt(np.mean((cpu - snap) ** 2)))

print()
print("=== MANUAL LAYERNORM SNAPDRAGON VALIDATION ===")
print("CPU shape:", cpu.shape)
print("Snapdragon shape:", snap.shape)
print("CPU first 8:", cpu.reshape(-1)[:8])
print("Snapdragon first 8:", snap.reshape(-1)[:8])
print("Max absolute error:", max_abs)
print("Mean absolute error:", mean_abs)
print("RMSE:", rmse)
print("Snapdragon min:", float(np.min(snap)))
print("Snapdragon max:", float(np.max(snap)))
print("Snapdragon mean:", float(np.mean(snap)))
print("Snapdragon std:", float(np.std(snap)))
print("OUTPUT SAVED:", out_file)

