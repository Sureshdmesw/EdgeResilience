from pathlib import Path
import qai_hub as hub

ROOT = Path(r"E:\EdgeResilience")

model = ROOT / "experiments" / "v4_manual_layernorm_diagnostic.onnx"

device = hub.Device("Snapdragon X Elite CRD")

job = hub.submit_compile_job(
    model=str(model),
    device=device,
    input_specs={
        "/ReduceSum_output_0": ((1,64), "float32")
    },
    name="EdgeResilience V4 Manual LayerNorm Diagnostic"
)

print("COMPILE JOB:", job.job_id)

job.wait()

target = job.get_target_model()

print("COMPILE COMPLETE")
print("TARGET MODEL:", target)
print("TARGET MODEL ID:", target.model_id)
