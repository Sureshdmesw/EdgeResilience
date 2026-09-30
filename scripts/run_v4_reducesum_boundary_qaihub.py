from pathlib import Path
import hashlib
import json
import numpy as np
import qai_hub as hub

ROOT = Path(r"E:\EdgeResilience")

model = ROOT / "experiments" / "v4_reducesum_boundary_diagnostic.onnx"
input_file = ROOT / "experiments" / "v4_snapdragon_control_input.npy"

print("MODEL:", model)
print("SIZE:", model.stat().st_size)

x = np.load(input_file).astype(np.float32)

print("INPUT:", input_file)
print("INPUT SHAPE:", x.shape)
print("INPUT DTYPE:", x.dtype)
print("INPUT SHA256:",
      hashlib.sha256(input_file.read_bytes()).hexdigest())

print()
print("Submitting ReduceSum boundary compile...")

compile_job = hub.submit_compile_job(
    model=str(model),
    device=hub.Device("Snapdragon X Elite CRD"),
    input_specs={
        "vehicle_temporal_features": ((1, 12, 17), "float32")
    },
    name="EdgeResilience V4 ReduceSum Boundary Diagnostic"
)

print("COMPILE JOB:", compile_job.job_id)

compile_job.wait()

target_model = compile_job.get_target_model()

print()
print("COMPILE COMPLETE")
print("TARGET MODEL:", target_model)
print("TARGET MODEL ID:", target_model.model_id)

print()
print("Submitting Snapdragon inference...")

inference_job = hub.submit_inference_job(
    model=target_model,
    device=hub.Device("Snapdragon X Elite CRD"),
    inputs={
        "vehicle_temporal_features": [x]
    },
    name="EdgeResilience V4 ReduceSum Boundary Inference"
)

print("INFERENCE JOB:", inference_job.job_id)

inference_job.wait()

output_data = inference_job.download_output_data()

print()
print("OUTPUT KEYS:", list(output_data.keys()))

for name, values in output_data.items():

    arr = np.asarray(values, dtype=np.float32)

    print()
    print("OUTPUT NAME:", name)
    print("OUTPUT SHAPE:", arr.shape)
    print("OUTPUT DTYPE:", arr.dtype)

    print("FIRST 8 VALUES:")
    print(arr.reshape(-1)[:8])

    print("MIN:", float(arr.min()))
    print("MAX:", float(arr.max()))
    print("MEAN:", float(arr.mean()))
    print("STD:", float(arr.std()))

    output_file = ROOT / "experiments" / "v4_reducesum_boundary_snapdragon_output.npy"

    np.save(output_file, arr)

    print()
    print("SNAPDRAGON OUTPUT SAVED:", output_file)

    report = {
        "compile_job_id": compile_job.job_id,
        "target_model_id": target_model.model_id,
        "inference_job_id": inference_job.job_id,
        "input_sha256": hashlib.sha256(
            input_file.read_bytes()
        ).hexdigest(),
        "output_name": name,
        "shape": list(arr.shape),
        "min": float(arr.min()),
        "max": float(arr.max()),
        "mean": float(arr.mean()),
        "std": float(arr.std()),
        "first_8": arr.reshape(-1)[:8].tolist()
    }

    report_file = ROOT / "experiments" / "v4_reducesum_boundary_snapdragon_result.json"

    report_file.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8"
    )

    print("REPORT:", report_file)
