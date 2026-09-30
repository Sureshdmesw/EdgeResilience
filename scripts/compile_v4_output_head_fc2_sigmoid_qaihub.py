from pathlib import Path
import qai_hub as hub

ROOT = Path(r"E:\EdgeResilience")

model = ROOT / "experiments" / "v4_output_head_fc2_sigmoid_diagnostic.onnx"

print("MODEL:", model)
print("EXISTS:", model.exists())
print("SIZE:", model.stat().st_size)

job = hub.submit_compile_job(
    model=str(model),
    device=hub.Device("Snapdragon X Elite CRD"),
    input_specs={
        "/output_head/output_head.2/Mul_1_output_0": ((1, 32), "float32")
    },
    name="EdgeResilience V4 FC2 Sigmoid Diagnostic"
)

print("COMPILE JOB:", job.job_id)

job.wait()

target = job.get_target_model()

print()
print("COMPILE COMPLETE")
print("TARGET MODEL:", target)
print("TARGET MODEL ID:", target.model_id)
