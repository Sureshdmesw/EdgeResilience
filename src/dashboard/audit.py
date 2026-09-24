import hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DASH = ROOT / "src" / "dashboard"

h = (DASH/"_part1_head.html").read_text("utf-8") + \
    (DASH/"_part2_body.html").read_text("utf-8") + \
    (DASH/"_part3_pages.html").read_text("utf-8")

def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

checks = [
    ("Product identity",          "EdgeResilience" in h),
    ("Snapdragon tagline",        "Snapdragon-Powered" in h),
    ("OBSERVE/PREDICT flow",      "Observe" in h and "Predict" in h and "Assess" in h),
    ("V4 Temporal Predictor",     "V4 Temporal Predictor" in h),
    ("MAE 0.0051",                "0.0051" in h),
    ("RMSE 0.0066",               "0.0066" in h),
    ("71,170 params",             "71,170" in h),
    ("Three cycles",              "cycle-001" in h and "cycle-002" in h and "cycle-003" in h),
    ("Risk policy named",         "V4_DEGRADATION_DEMO_POLICY_V1" in h),
    ("Policy disclaimer",         "Demonstration policy" in h),
    ("Connectivity page",         "page-resilience" in h),
    ("Evidence page",             "page-evidence" in h),
    ("Deployment page",           "page-deploy" in h),
    ("Explorer page",             "page-system" in h),
    ("NOT VERIFIED shown",        "NOT VERIFIED" in h),
    ("CPU-to-CPU honest",         "CPU-to-CPU" in h),
    ("5.99x speedup",             "5.99" in h),
    ("SHA-256 checksum shown",    "b551ad9f" in h),
    ("Safety boundary",           "SOFTWARE SIMULATION" in h),
    ("Physical vehicle NO",       "Physical vehicle" in h),
    ("External CAN NO",           "External CAN" in h),
    ("Live demo page",            "page-demo" in h),
    ("stepDemo JS",               "stepDemo" in h),
    ("Provenance section",        "Provenance" in h),
    ("FUTURE roadmap",            "FUTURE" in h),
    ("AI/Deterministic sep",      "DETERMINISTIC POLICY" in h),
    ("Connectivity lifecycle",    "Resilience Lifecycle" in h),
    ("Deployment matrix",         "Deployment Status Matrix" in h),
    ("Roadmap items",             "Snapdragon Hardware Validation" in h),
    ("Safety no actuation",       "Direct actuation" in h),
]

print("=" * 55)
print("DASHBOARD QUALITY AUDIT")
print("=" * 55)
fails = 0
for name, ok in checks:
    print(("PASS" if ok else "FAIL"), name)
    if not ok:
        fails += 1

print()
print("=" * 55)
print("PROTECTED ARTIFACT CHECKSUMS")
print("=" * 55)
artifacts = [
    ("V4 Model",     ROOT/"models/edgeresilience/temporal_predictor_v4.pt",
                     "b551ad9f02b56668ef3f8f7873133748275307f1934ec7fd77da14e7325d26b9"),
    ("V4 Dataset",   ROOT/"data/processed/temporal/edgeresilience_temporal_dataset_v4.jsonl",
                     "02a82f0f5ee78dc4e3be28b81b53b6eb4eb884600a4734f3eb3aaa279cb3a911"),
    ("Dynamic ONNX", ROOT/"models/edgeresilience/temporal_predictor_v4_dynamic.onnx",
                     "acb43a20c9fa64577c56bdfe3aa3c2ea96b6691420c0a7994dc5fd9f230c0e5d"),
]
for name, path, expected in artifacts:
    actual = sha256(path)
    ok = actual.lower() == expected.lower()
    if not ok: fails += 1
    print(("PASS" if ok else "FAIL ***MISMATCH***"), name)

print()
print("=" * 55)
print("EVIDENCE DATA CHECK")
print("=" * 55)
ev = json.loads((ROOT/"data/evidence/v4_demo_scenario.json").read_text("utf-8"))
print("Cycles:", len(ev["cycles"]))
for c in ev["cycles"]:
    pred = c["prediction"]["predicted_future_degradation"]
    print(f"  {c['cycle_id']}  conn={c['connectivity_state']}  risk={c['risk']['predictive_risk_level']}  deg={pred:.4f}")

print()
print("=" * 55)
print("FINAL RESULT:", "ALL PASS" if fails == 0 else f"{fails} FAILURES")
print("=" * 55)
print("Launch: python src/dashboard/server.py")
print("Open  : http://127.0.0.1:8765")


