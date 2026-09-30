from pathlib import Path
import hashlib
import json
import numpy as np
import qai_hub as hub

ROOT = Path(r"E:\EdgeResilience")

model = ROOT / "experiments" / "v4_output_head_sigmoid_diagnostic.onnx"
input_file = ROOT / "experiments" / "v4_fc2_snapdragon_exact_output.npy"
cpu_reference_file = ROOT / "experiments" / "v4_output_head_sigmoid_cpu_output.npy"

x = np.load(input_file).astype(np.float32)
cpu_reference = np.load(cpu_reference_file).astype(np.float32)

print("INPUT:", x)
print("INPUT SHAPE:", x.shape)
print("INPUT SHA256:",
      hashlib.sha256(input_file.read_bytes()).hexdigest())

print()
print("CPU SIGMOID REFERENCE:", cpu_reference)
print("CPU SIGMOID:", float(cpu_reference.reshape(-1)[0]))

print()
print("Submitting compile job...")

compile_job = hub.submit_compile_job(
    model=str(model),
    device=hub.Device("Snapdragon X Elite CRD"),
    input_specs={
        "fc2_output": ((1, 1), "float32")
    },
    name="EdgeResilience V4 Sigmoid Exact-FC2 Diagnostic"
)

print("COMPILE JOB:", compile_job.job_id)

compile_job.wait()

target_model = compile_job.get_target_model()

print("TARGET MODEL:", target_model)
print("TARGET MODEL ID:", target_model.model_id)

print()
print("Submitting inference...")

inference_job = hub.submit_inference_job(
    model=target_model,
    device=hub.Device("Snapdragon X Elite CRD"),
    inputs={
        "fc2_output": [x]
    },
    name="EdgeResilience V4 Sigmoid Exact-FC2 Inference"
)

print("INFERENCE JOB:", inference_job.job_id)

inference_job.wait()

output_data = inference_job.download_output_data()

print("OUTPUT KEYS:", list(output_data.keys()))

for name, values in output_data.items():

    snap = np.asarray(values, dtype=np.float32)

    print()
    print("OUTPUT NAME:", name)
    print("SNAPDRAGON SIGMOID:", snap)
    print("SHAPE:", snap.shape)

    snap_scalar = float(snap.reshape(-1)[0])
    cpu_scalar = float(cpu_reference.reshape(-1)[0])

    abs_error = abs(snap_scalar - cpu_scalar)
    rel_error = abs_error / max(abs(cpu_scalar), 1e-12)

    print()
    print("CPU SIGMOID:", cpu_scalar)
    print("SNAPDRAGON SIGMOID:", snap_scalar)
    print("ABS ERROR:", abs_error)
    print("RELATIVE ERROR:", rel_error)
    print("RELATIVE ERROR %:", rel_error * 100)

    report = {
        "compile_job_id": compile_job.job_id,
        "target_model_id": target_model.model_id,
        "inference_job_id": inference_job.job_id,
        "input_fc2_snapdragon": float(x.reshape(-1)[0]),
        "cpu_sigmoid_reference": cpu_scalar,
        "snapdragon_sigmoid": snap_scalar,
        "absolute_error": abs_error,
        "relative_error": rel_error,
        "relative_error_percent": rel_error * 100
    }

    report_file = ROOT / "experiments" / "v4_sigmoid_exact_snapdragon_fc2_result.json"

    report_file.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8"
    )

    print("REPORT:", report_file)
