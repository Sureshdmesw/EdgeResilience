import qai_hub as hub
from pathlib import Path

MODEL = Path(r"E:\EdgeResilience\experiments\v4_final_plus_layernorm_trace_static.onnx")

device = hub.Device(
    name="Snapdragon X Elite CRD"
)

print("=== V4 FINAL + LAYERNORM TRACE COMPILE ===")
print(f"Model: {MODEL}")
print(f"Device: {device}")

job = hub.submit_compile_job(
    model=str(MODEL),
    device=device,
)

print(f"Compile Job ID: {job.job_id}")

job.wait()

print("Compile job completed.")

try:
    target_model = job.get_target_model()
    print(f"Target model: {target_model}")
except Exception as e:
    print(f"Could not retrieve target model: {e}")
