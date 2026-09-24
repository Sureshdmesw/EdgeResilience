from qai_hub import Client

client = Client()

compile_job_id = "jp0mjdr2g"
profile_job_id = "jp3z9xmx5"

compile_job = client.get_job(compile_job_id)
profile_job = client.get_job(profile_job_id)

print("=" * 70)
print("QUALCOMM AI HUB JOB VALIDATION")
print("=" * 70)

print("\n[COMPILE JOB]")
print("Job ID :", compile_job.job_id)
print("Name   :", compile_job.name)
print("Type   :", type(compile_job).__name__)

print("\n[COMPILE TARGET SHAPES]")
try:
    print(compile_job.get_target_shapes())
except Exception as e:
    print("Target-shape query failed:", e)

print("\n[COMPILE TARGET MODEL]")
try:
    target = compile_job.get_target_model()
    print(target)
except Exception as e:
    print("Target-model query failed:", e)

print("\n[PROFILE JOB]")
print("Job ID :", profile_job.job_id)
print("Name   :", profile_job.name)
print("Type   :", type(profile_job).__name__)

print("\n[PROFILE STATUS]")
try:
    print(profile_job.status)
except Exception as e:
    print("Status attribute unavailable:", e)
    try:
        print("State:", profile_job.state)
    except Exception:
        print("No direct state attribute available.")

print("\n" + "=" * 70)
print("QUALCOMM AI HUB VALIDATION CHECK COMPLETE")
print("=" * 70)
