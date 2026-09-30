import qai_hub as hub

MODEL = r"experiments\v4_fp32_boundary_probe_static.onnx"

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

print("COMPILE JOB FINISHED")

try:
    target = job.get_target_model()
    print("TARGET MODEL:", target.model_id)
except Exception as e:
    print("TARGET MODEL ERROR:", repr(e))
