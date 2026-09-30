import json
from pathlib import Path
from datetime import datetime, timezone

p = Path(r"experiments\snapdragon\snapdragon_deployment_manifest.json")

with p.open("r", encoding="utf-8") as f:
    data = json.load(f)

# Hardware actually verified on Snapdragon X Elite CRD.
data["hardware"]["snapdragon_present"] = True
data["hardware"]["device"] = "Snapdragon X Elite CRD"
data["hardware"]["soc"] = "SC8380XP"
data["hardware"]["os"] = "Windows 11"
data["hardware"]["npu"] = "Qualcomm QNN / HTP"
data["hardware"]["memory"] = "28.5 MB peak during full V4 profile"

# Backend verification is now established at full-production profile level.
for backend in data["backends"]:
    if backend["name"] == "qualcomm_qnn_htp_npu":
        backend["verified"] = True
        backend["status"] = "FULL_PRODUCTION_PROFILE_VERIFIED"
        backend["profile_job"] = "jpxlwmxlp"
        backend["target_model"] = "mn75w5l8m"
        backend["npu_layers"] = 90

# Hardware NPU execution status.
data["npu_status"] = "VERIFIED_FULL_PRODUCTION_PROFILE"

data["snapdragon_execution_status"] = (
    "VERIFIED_ON_SNAPDRAGON_X_ELITE_CRD_VIA_QNN_HTP"
)

# Keep QNN conversion wording intact because the deployed artifact
# was profiled through the existing QAI Hub target model.
data["qnn_conversion_status"] = "QNN_READY_MODEL_PROFILE_VERIFIED"

# Preserve CPU/reference equivalence results and explicitly record
# the hardware numerical-equivalence result.
data["numerical_equivalence"]["qnn_execution_vs_reference"] = {
    "result": "FAIL",
    "source": "experiments/v4_cpu_snapdragon_numerical_equivalence.json",
    "max_absolute_error": 0.0030923495069146156,
    "mean_absolute_error": 0.0030923495069146156,
    "max_relative_error": 0.3850368154560905
}

# Production V4 performance evidence.
data["performance"]["snapdragon_npu_latency_ms"] = 0.063
data["performance"]["snapdragon_npu_warm_median_latency_ms"] = 0.067
data["performance"]["snapdragon_npu_warm_mean_latency_ms"] = 0.06895959595959596
data["performance"]["snapdragon_npu_p90_latency_ms"] = 0.077
data["performance"]["snapdragon_npu_p95_latency_ms"] = 0.082
data["performance"]["snapdragon_npu_p99_latency_ms"] = 0.088
data["performance"]["throughput_snapdragon_samples_per_sec"] = 14501.245056393731
data["performance"]["throughput_snapdragon_warm_median_samples_per_sec"] = 14925.373134328358
data["performance"]["throughput_note"] = (
    "Profile-derived single-batch warm timing; not a separately measured sustained throughput benchmark."
)

# Resource evidence.
data["resource_measurements"]["memory_footprint_mb"] = 28.5
data["resource_measurements"]["power_watts"] = "NOT VERIFIED"
data["resource_measurements"]["thermal"] = "NOT VERIFIED"

# Full-production profile lineage.
data["profile_evidence"] = {
    "profile_job": "jpxlwmxlp",
    "target_model": "mn75w5l8m",
    "device": "Snapdragon X Elite CRD",
    "estimated_inference_time_us": 63,
    "warm_sample_count": 99,
    "npu_execution_entries": 90,
    "npu_execution_coverage": "100% of profiled execution entries",
    "htp_utilization_percent": "NOT EXPOSED BY QAI HUB PROFILE",
    "peak_memory_mb": 28.5
}

# Important: Snapdragon execution is verified, but numerical equivalence is not.
data["overall_status"] = (
    "SNAPDRAGON_FULL_PRODUCTION_HTP_PROFILE_VERIFIED_"
    "NUMERICAL_EQUIVALENCE_FAIL_POWER_THERMAL_UNVERIFIED"
)

data["validation_timestamp"] = datetime.now(timezone.utc).isoformat()

with p.open("w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print("UPDATED:", p)
