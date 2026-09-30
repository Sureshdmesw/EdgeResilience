from pathlib import Path
import hashlib
import json
import numpy as np
import qai_hub as hub

ROOT = Path(r"E:\EdgeResilience")

model = ROOT / "experiments" / "v4_output_head_fc2_diagnostic.onnx"
input_file = ROOT / "experiments" / "v4_output_head_gelu_cpu_output.npy"
cpu_output_file = ROOT / "experiments" / "v4_output_head_fc2_cpu_output.npy"

x = np.load(input_file).astype(np.float32)
cpu = np.load(cpu_output_file).astype(np.float32)

print("MODEL:", model)
print("INPUT:", input_file)
print("INPUT SHAPE:", x.shape)
print("INPUT SHA256:", hashlib.sha256(input_file.read_bytes()).hexdigest())
print("CPU FC2 OUTPUT:", cpu)
print("CPU FC2 SCALAR:", float(cpu.reshape(-1)[0]))

print()
print("Submitting compile job...")

compile_job = hub.submit_compile_job(
    model=str(model),
    device=hub.Device("Snapdragon X Elite CRD"),
    input_specs={
        "/output_head/output_head.2/Mul_1_output_0": ((1, 32), "float32")
    },
    name="EdgeResilience V4 FC2 Diagnostic"
)

print("COMPILE JOB:", compile_job.job_id)

compile_job.wait()


target_model = compile_job.get_target_model()

print("TARGET MODEL:", target_model)
print("TARGET MODEL ID:", target_model.model_id)

print()
print("Submitting FC2 inference...")

inputs = {
    "/output_head/output_head.2/Mul_1_output_0": [x]
}

inference_job = hub.submit_inference_job(
    model=target_model,
    device=hub.Device("Snapdragon X Elite CRD"),
    inputs=inputs,
    name="EdgeResilience V4 FC2 Diagnostic Inference"
)

print("INFERENCE JOB:", inference_job.job_id)

inference_job.wait()


output_data = inference_job.download_output_data()

print("OUTPUT KEYS:", list(output_data.keys()))

for name, values in output_data.items():

    arr = np.asarray(values, dtype=np.float32)

    print()
    print("OUTPUT NAME:", name)
    print("SNAPDRAGON FC2:", arr)
    print("SHAPE:", arr.shape)

    cpu_scalar = float(cpu.reshape(-1)[0])
    snap_scalar = float(arr.reshape(-1)[0])

    abs_error = abs(snap_scalar - cpu_scalar)
    rel_error = abs_error / max(abs(cpu_scalar), 1e-12)

    print()
    print("CPU FC2:", cpu_scalar)
    print("SNAPDRAGON FC2:", snap_scalar)
    print("ABS ERROR:", abs_error)
    print("RELATIVE ERROR:", rel_error)
    print("RELATIVE ERROR %:", rel_error * 100)

    report = {
        "compile_job_id": compile_job.job_id,
        "target_model_id": target_model.model_id,
        "inference_job_id": inference_job.job_id,
        "input_sha256": hashlib.sha256(
            input_file.read_bytes()
        ).hexdigest(),
        "cpu_fc2": cpu_scalar,
        "snapdragon_fc2": snap_scalar,
        "absolute_error": abs_error,
        "relative_error": rel_error,
        "relative_error_percent": rel_error * 100
    }

    report_file = ROOT / "experiments" / "v4_output_head_fc2_snapdragon_result.json"

    report_file.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8"
    )

    print("REPORT:", report_file)
