from pathlib import Path
import hashlib
import json
import numpy as np
import qai_hub as hub

ROOT = Path(r"E:\EdgeResilience")

model = ROOT / "models" / "edgeresilience" / "snapdragon" / "temporal_predictor_v4_qnn_ready.onnx"
input_file = ROOT / "experiments" / "v4_snapdragon_control_input.npy"

x = np.load(input_file).astype(np.float32)

print("MODEL:", model)
print("INPUT:", input_file)
print("INPUT SHAPE:", x.shape)
print("INPUT SHA256:",
      hashlib.sha256(input_file.read_bytes()).hexdigest())

print()
print("Submitting ORIGINAL QNN-ready compile...")

compile_job = hub.submit_compile_job(
    model=str(model),
    device=hub.Device("Snapdragon X Elite CRD"),
    input_specs={
        "vehicle_temporal_features": ((1, 12, 17), "float32")
    },
    name="EdgeResilience V4 QNN Ready Reproducibility"
)

print("COMPILE JOB:", compile_job.job_id)

compile_job.wait()

target_model = compile_job.get_target_model()

print("TARGET MODEL:", target_model)
print("TARGET MODEL ID:", target_model.model_id)

print()
print("Submitting ORIGINAL FULL MODEL inference...")

inference_job = hub.submit_inference_job(
    model=target_model,
    device=hub.Device("Snapdragon X Elite CRD"),
    inputs={
        "vehicle_temporal_features": [x]
    },
    name="EdgeResilience V4 QNN Ready Reproducibility Inference"
)

print("INFERENCE JOB:", inference_job.job_id)

inference_job.wait()

output_data = inference_job.download_output_data()

print()
print("OUTPUT KEYS:", list(output_data.keys()))

for name, values in output_data.items():

    arr = np.asarray(values, dtype=np.float32)

    print()
    print("OUTPUT:", name)
    print("SHAPE:", arr.shape)
    print("VALUE:", arr)
    print("SCALAR:", float(arr.reshape(-1)[0]))

    report = {
        "compile_job_id": compile_job.job_id,
        "target_model_id": target_model.model_id,
        "inference_job_id": inference_job.job_id,
        "input_sha256": hashlib.sha256(
            input_file.read_bytes()
        ).hexdigest(),
        "output_name": name,
        "output": arr.tolist(),
        "scalar": float(arr.reshape(-1)[0])
    }

    report_file = (
        ROOT / "experiments" /
        "v4_qnn_ready_reproducibility_result.json"
    )

    report_file.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8"
    )

    print("REPORT:", report_file)
