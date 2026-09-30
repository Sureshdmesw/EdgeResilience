from pathlib import Path
import qai_hub as hub

model = Path(r"E:\EdgeResilience\experiments\v4_output_head_tanh_diagnostic.onnx")

device = hub.Device("Snapdragon X Elite CRD")

job = hub.submit_compile_job(
    model=str(model),
    device=device,
    input_specs={
        "/ReduceSum_output_0": ((1,64), "float32")
    },
    name="EdgeResilience V4 Output Head Tanh GELU Diagnostic"
)

print("JOB:", job)
print("JOB ID:", job.job_id)

job.wait()

print("STATUS:", job.status)

if job.status != "SUCCESS":
    print(job)
    raise SystemExit(1)

target = job.get_target_model()
print("TARGET MODEL:", target)
print("TARGET MODEL ID:", target.model_id)
