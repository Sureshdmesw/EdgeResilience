import qai_hub as hub
import inspect

job = hub.get_job("jpxlwmxlp")

print("=" * 80)
print("PROFILE JOB SDK API")
print("=" * 80)

print("CLASS:", type(job))
print("MODULE:", type(job).__module__)

print("\n=== PUBLIC METHODS / ATTRIBUTES ===")
for name in sorted(dir(job)):
    if not name.startswith("_"):
        try:
            value = getattr(job, name)
            if callable(value):
                try:
                    sig = inspect.signature(value)
                except Exception:
                    sig = "(signature unavailable)"
                print(f"{name}{sig}")
            else:
                print(f"{name} = {value!r}")
        except Exception as e:
            print(f"{name} <ERROR: {e}>")

print("\n=== ARTIFACT API REFERENCES ===")
for name in sorted(dir(job)):
    if any(x in name.lower() for x in ["artifact", "profile", "trace", "download", "result", "summary"]):
        print(name)
