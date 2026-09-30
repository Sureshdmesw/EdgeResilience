import qai_hub as hub

MODEL = r"experiments\v4_output_head_diagnostic.onnx"

devices = hub.get_devices(name="Snapdragon X Elite CRD")
if not devices:
    raise RuntimeError("Snapdragon X Elite CRD not found")

device = devices[0]

print("DEVICE:", device)

job = hub.submit_compile_job(
    model=MODEL,
    device=device
)

print("COMPILE JOB:", job.job_id)

job.wait()

print("COMPILE COMPLETE")

try:
    target = job.get_target_model()
    print("TARGET MODEL:", target.model_id)
except Exception as e:
    print("TARGET MODEL ERROR:", repr(e))
