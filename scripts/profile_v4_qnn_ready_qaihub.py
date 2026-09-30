import qai_hub as hub

target_model = hub.get_job("jp1n962kg").get_target_model()
device = hub.Device("Snapdragon X Elite CRD")

print("=" * 80)
print("EDGERESILIENCE V4 QNN-READY HTP PROFILE")
print("=" * 80)
print("Target model:", target_model)
print("Device:", device.name)

job = hub.submit_profile_job(
    model=target_model,
    device=device,
    name="EdgeResilience V4 QNN-Ready Full Model HTP Profile"
)

print("PROFILE_JOB_ID:", job.job_id)

status = job.wait()

print("STATUS:", status)
print("AVAILABLE_ARTIFACTS:", job.get_available_artifacts())
