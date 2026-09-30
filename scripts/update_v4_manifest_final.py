import json
from pathlib import Path

p = Path(r"experiments\snapdragon_deployment_manifest_v4.json")

with p.open("r", encoding="utf-8") as f:
    data = json.load(f)

data["full_model"]["htp_verified"] = True
data["full_model"]["htp_profile_job"] = "jpxlwmxlp"
data["full_model"]["htp_inference_ms"] = 0.063
data["full_model"]["npu_layers"] = 90
data["full_model"]["peak_memory_mb"] = 28.5
data["full_model"]["numerical_equivalence"] = "FAIL"
data["full_model"]["numerical_equivalence_source"] = (
    "experiments/v4_cpu_snapdragon_numerical_equivalence.json"
)

# Remove the obsolete failure statement.
data["full_model"].pop("htp_failure", None)

data["performance"] = {
    "estimated_inference_ms": 0.063,
    "warm_median_ms": 0.067,
    "warm_mean_ms": 0.06895959595959596,
    "p90_ms": 0.077,
    "p95_ms": 0.082,
    "p99_ms": 0.088,
    "warm_mean_inferences_per_sec": 14501.245056393731,
    "warm_median_inferences_per_sec": 14925.373134328358,
    "peak_memory_mb": 28.5,
    "htp_utilization_percent": "NOT EXPOSED BY QAI HUB PROFILE",
    "power_watts": "NOT VERIFIED",
    "thermal": "NOT VERIFIED"
}

data["status"] = (
    "SNAPDRAGON_FULL_MODEL_HTP_PROFILE_VERIFIED_"
    "NUMERICAL_EQUIVALENCE_FAIL_POWER_THERMAL_UNVERIFIED"
)

with p.open("w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print("UPDATED:", p)
