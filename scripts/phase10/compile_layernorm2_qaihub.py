import qai_hub as hub
from pathlib import Path

model_path = Path(
    r"E:\EdgeResilience\models\edgeresilience\snapdragon\v4_diag_layernorm2.onnx"
)

device = hub.Device("Snapdragon X Elite CRD")

print("Model:", model_path)
print("Device:", device.name)

job = hub.submit_compile_job(
    model=str(model_path),
    device=device,
    input_specs={
        "add_3": ((1, 12, 64), "float32")
    },
    name="EdgeResilience V4 LayerNorm2 Diagnostic"
)

print("JOB_ID:", job.job_id)

status = job.wait()
print("STATUS:", status)

print("TARGET_MODEL:", job.get_target_model())
