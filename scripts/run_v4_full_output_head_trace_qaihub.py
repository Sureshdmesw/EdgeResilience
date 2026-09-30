from pathlib import Path
import hashlib
import json
import numpy as np
import qai_hub as hub

ROOT = Path(r"E:\EdgeResilience")

model = ROOT / "experiments" / "v4_full_output_head_trace.onnx"
input_file = ROOT / "experiments" / "v4_snapdragon_control_input.npy"

x = np.load(input_file).astype(np.float32)

print("MODEL:", model)
print("MODEL SIZE:", model.stat().st_size)
print("INPUT:", input_file)
print("INPUT SHAPE:", x.shape)
print("INPUT SHA256:",
      hashlib.sha256(input_file.read_bytes()).hexdigest())

print()
print("Submitting trace compile...")

compile_job = hub.submit_compile_job(
    model=str(model),
    device=hub.Device("Snapdragon X Elite CRD"),
    input_specs={
        "vehicle_temporal_features": ((1, 12, 17), "float32")
    },
    name="EdgeResilience V4 Full Output Head Trace V2"
)

print("COMPILE JOB:", compile_job.job_id)

compile_job.wait()

target_model = compile_job.get_target_model()

print()
print("COMPILE COMPLETE")
print("TARGET MODEL:", target_model)
print("TARGET MODEL ID:", target_model.model_id)

print()
print("Submitting trace inference...")

inference_job = hub.submit_inference_job(
    model=target_model,
    device=hub.Device("Snapdragon X Elite CRD"),
    inputs={
        "vehicle_temporal_features": [x]
    },
    name="EdgeResilience V4 Full Output Head Trace V2 Inference"
)

print("INFERENCE JOB:", inference_job.job_id)

inference_job.wait()

output_data = inference_job.download_output_data()

print()
print("OUTPUT KEYS:", list(output_data.keys()))

report = {
    "compile_job_id": compile_job.job_id,
    "target_model_id": target_model.model_id,
    "inference_job_id": inference_job.job_id,
    "input_sha256": hashlib.sha256(
        input_file.read_bytes()
    ).hexdigest(),
    "outputs": {}
}

for name, values in output_data.items():

    arr = np.asarray(values, dtype=np.float32)
    flat = arr.reshape(-1)

    print()
    print("=" * 72)
    print("OUTPUT:", name)
    print("SHAPE:", arr.shape)
    print("DTYPE:", arr.dtype)
    print("FIRST 8:", flat[:8])
    print("MIN:", float(arr.min()))
    print("MAX:", float(arr.max()))
    print("MEAN:", float(arr.mean()))
    print("STD:", float(arr.std()))

    safe_name = (
        name.replace("/", "_")
            .replace("\\", "_")
            .replace(":", "_")
    )

    output_file = (
        ROOT / "experiments" /
        f"v4_full_trace_snapdragon_{safe_name}.npy"
    )

    np.save(output_file, arr)

    print("SAVED:", output_file)

    report["outputs"][name] = {
        "shape": list(arr.shape),
        "dtype": str(arr.dtype),
        "first_8": flat[:8].tolist(),
        "min": float(arr.min()),
        "max": float(arr.max()),
        "mean": float(arr.mean()),
        "std": float(arr.std()),
        "file": str(output_file)
    }

report_file = (
    ROOT / "experiments" /
    "v4_full_output_head_trace_result.json"
)

report_file.write_text(
    json.dumps(report, indent=2),
    encoding="utf-8"
)

print()
print("=" * 72)
print("TRACE COMPLETE")
print("REPORT:", report_file)
