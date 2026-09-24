import qai_hub as hub
import numpy as np
from pathlib import Path

target_model = "mn1lje3rq"
inputs_path = Path(
    r"E:\EdgeResilience\artifacts\phase10\qualcomm_inference\v4_multi_hw_inputs.npz"
)

data = np.load(inputs_path)

inputs = {
    "add_3": [data[k].astype(np.float32) for k in data.files]
}

print("TARGET MODEL:", target_model)
print("INPUT COUNT:", len(inputs["add_3"]))
print("INPUT SHAPES:", [x.shape for x in inputs["add_3"]])

device = hub.Device("Snapdragon X Elite CRD")

job = hub.submit_inference_job(
    model=hub.get_model(target_model),
    device=device,
    inputs=inputs,
    name="EdgeResilience V4 LayerNorm2 Five Input Validation",
)

print("JOB_ID:", job.job_id)

status = job.wait()
print("STATUS:", status)

dataset = job.get_output_dataset()
print("OUTPUT_DATASET:", dataset)

out_dir = Path(
    r"E:\EdgeResilience\artifacts\phase10\qualcomm_inference\layernorm2_snapdragon"
)
out_dir.mkdir(parents=True, exist_ok=True)

downloaded = dataset.download(str(out_dir))
print("DOWNLOADED:", downloaded)
