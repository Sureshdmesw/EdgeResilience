import qai_hub as hub
from pathlib import Path

job_id = "jp8ex6yqp"
out = Path("experiments/snapdragon/profile_artifacts/v4_temporal_pooling")
out.mkdir(parents=True, exist_ok=True)

client = hub.Client()
job = client.get_job(job_id)

print("JOB:", job)
print("STATUS:", job.get_status())
print("ARTIFACTS:", job.get_available_artifacts())

for artifact_type in job.get_available_artifacts():
    print()
    print("DOWNLOADING:", artifact_type)
    try:
        result = job.download_results(
            artifact_type=artifact_type,
            output_dir=str(out),
        )
        print("RESULT:", result)
    except Exception as e:
        print("DOWNLOAD ERROR:", repr(e))
