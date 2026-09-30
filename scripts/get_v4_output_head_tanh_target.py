import qai_hub as hub

job = hub.get_job("jp2r2ylqg")

print("JOB:", job)
print("JOB TYPE:", type(job).__name__)

target = job.get_target_model()

print("TARGET MODEL:", target)
print("TARGET MODEL ID:", target.model_id)
