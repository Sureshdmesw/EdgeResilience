from pathlib import Path
import qai_hub as hub

ROOT = Path(r"E:\EdgeResilience")

model_path = ROOT / "experiments" / "v4_output_head_diagnostic.onnx"

device = hub.Device("Snapdragon X Elite CRD")

job = hub.submit_compile_job(
    model=str(model_path),
    device=device,
    input_specs={
        "/ReduceSum_output_0": ((1, 64), "float32")
    },
    name="EdgeResilience V4 Output Head Diagnostic",
)

print("COMPILE JOB:", job.job_id)

status = job.wait()

print("STATUS:")
print(status)

target = job.get_target_model()

print("TARGET MODEL:", target)
print("TARGET MODEL ID:", target.model_id)
