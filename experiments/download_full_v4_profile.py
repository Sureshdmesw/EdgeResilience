import qai_hub as hub
from pathlib import Path

job = hub.get_job("jpxlwmxlp")

out = Path(r"experiments\snapdragon\profile_artifacts\v4_full_production")
out.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("DOWNLOADING FULL PRODUCTION V4 PROFILE")
print("=" * 80)

print("JOB:", job.job_id)
print("STATUS:", job.get_status())
print("ARTIFACTS:", job.get_available_artifacts())

result = job.download_results(str(out))

print("\nRESULT TYPE:", type(result))
print("RESULT:", result)

print("\n=== DOWNLOADED FILES ===")
for p in sorted(out.rglob("*")):
    if p.is_file():
        print(f"{p}  ({p.stat().st_size} bytes)")
