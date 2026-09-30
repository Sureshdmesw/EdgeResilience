import qai_hub as hub
from pathlib import Path

model_path = Path(
    r"E:\EdgeResilience\models\edgeresilience\snapdragon\temporal_predictor_v4_qnn_ready.onnx"
)

device = hub.Device("Snapdragon X Elite CRD")

print("=" * 80)
print("EDGERESILIENCE V4 QNN-READY FULL-MODEL COMPILE")
print("=" * 80)
print("Model :", model_path)
print("Device:", device.name)

job = hub.submit_compile_job(
    model=str(model_path),
    device=device,
    input_specs={
        "vehicle_temporal_features": ((1, 12, 17), "float32")
    },
    name="EdgeResilience V4 QNN-Ready Full Model"
)

print("JOB_ID:", job.job_id)

status = job.wait()

print("STATUS:", status)
print("TARGET_MODEL:", job.get_target_model())
