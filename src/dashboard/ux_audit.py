# -*- coding: utf-8 -*-
"""
EdgeResilience â€” UX Quality Audit
Checks product experience contracts, not just string presence.
Run: python src/dashboard/ux_audit.py
"""
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
    # â”€â”€ PRODUCT IDENTITY â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    ("Product identity visible",            "EdgeResilience" in h),
    ("Snapdragon tagline present",          "Snapdragon-Powered" in h),
    ("Competition context present",         "Qualcomm Snapdragon AI Lab" in h),
    ("Brand mark present",                  "brand-mark" in h),

    # â”€â”€ SYSTEM STATE VISIBILITY â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    ("Hero section present",                "class=\"hero\"" in h),
    ("State hero cards present",            "state-hero" in h),
    ("AI prediction card present",          "sc-deg-val" in h),
    ("Connectivity state card present",     "sc-conn-val" in h),
    ("Validation card present",             "sc-trust" in h),

    # â”€â”€ PREDICTIVE RISK VISIBILITY â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    ("Risk policy named",                   "V4_DEGRADATION_DEMO_POLICY_V1" in h),
    ("Policy is demonstration only",        "Demonstration policy" in h),
    ("Risk threshold map present",          "NORMAL" in h and "MEDIUM" in h and "CRITICAL" in h),
    ("MAE metric visible",                  "0.0051" in h),
    ("RMSE metric visible",                 "0.0066" in h),
    ("71170 params visible",                "71,170" in h),

    # â”€â”€ TEMPORAL VISUALIZATION â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    ("Temporal SVG element present",        "ai-temporal-svg" in h),
    ("Temporal visualization JS",           "renderTemporalSVG" in h),
    ("Observed/predicted boundary",         "PRED" in h or "predicted future" in h.lower()),
    ("12 steps explained",                  "12 steps" in h or "12 observation" in h),
    ("17 features explained",               "17 features" in h or "17 cyber" in h),

    # â”€â”€ CONNECTIVITY RESILIENCE â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    ("Connectivity resilience page",        "page-resilience" in h),
    ("Local intelligence message",          "LOCAL INTELLIGENCE CONTINUES" in h),
    ("Resilience lifecycle flow",           "Resilience Lifecycle" in h),
    ("Connectivity states shown",           "DISCONNECTED" in h and "CONNECTED" in h),
    ("Recovery detection explained",        "recovery_detected" in h or "Recovery detection" in h),

    # â”€â”€ EVIDENCE CHAIN â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    ("Evidence page present",               "page-evidence" in h),
    ("Trust layer present",                 "Trust" in h and "Verification" in h),
    ("SHA-256 integrity shown",             "SHA-256" in h),
    ("Evidence chain visual",               "Evidence Chain" in h),
    ("Expandable evidence rows",            "toggleEvRow" in h),
    ("Model checksum shown",                "b551ad9f" in h),

    # â”€â”€ DEPLOYMENT PROGRESSION â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    ("Deployment page present",             "page-deploy" in h),
    ("Deployment journey steps",            "Deployment Journey" in h),
    ("CPU verified shown",                  "CPU reference" in h and "VERIFIED" in h),
    ("ONNX verified shown",                 "ONNX" in h and "VERIFIED" in h),
    ("Snapdragon NOT VERIFIED honest",      "NOT VERIFIED" in h),
    ("CPU-to-CPU benchmark honest",         "CPU-to-CPU" in h),
    ("5.99x speedup shown",                 "5.99" in h),
    ("No false Snapdragon claim",           "NPU ACTIVE" not in h and "SNAPDRAGON VERIFIED" not in h),

    # â”€â”€ INTERACTIVE DEMO â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    ("Live demo page present",              "page-demo" in h),
    ("Next Cycle button present",           "Next Cycle" in h),
    ("Auto Play button present",            "autoPlay" in h),
    ("Reset button present",               "resetDemo" in h),
    ("State machine visual",                "sm-wrap" in h and "sm-dot" in h),
    ("Demo conclusion panel",               "demo-conclusion" in h),
    ("Demonstration complete message",      "Demonstration Complete" in h),
    ("stepDemo JS function",                "function stepDemo" in h),

    # â”€â”€ PROGRESSIVE DISCLOSURE â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    ("Accordion component present",         "acc-hd" in h and "acc-body" in h),
    ("toggleAcc JS function",               "function toggleAcc" in h),
    ("System explorer page",                "page-system" in h),
    ("Model card accordion",                "Model Card" in h),
    ("Data card accordion",                 "Data Card" in h),
    ("Provenance accordion",                "Provenance Register" in h),
    ("17 features expandable",              "explore-features" in h),

    # â”€â”€ RESPONSIVE LAYOUT â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    ("Responsive grid classes",             "g2" in h and "g3" in h and "g4" in h),
    ("Media queries present",               "@media" in h),
    ("Mobile viewport meta",                "width=device-width" in h),

    # â”€â”€ ACCESSIBILITY â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    ("ARIA labels on nav",                  "aria-label" in h),
    ("aria-live on demo status",            "aria-live" in h),
    ("aria-expanded on accordions",         "aria-expanded" in h),
    ("Semantic button elements",            "<button" in h),
    ("Reduced motion support",              "prefers-reduced-motion" in h),

    # â”€â”€ PRESENTATION MODE â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    ("Presentation mode button",            "pres-btn" in h),
    ("togglePresMode JS function",          "function togglePresMode" in h),

    # â”€â”€ SEMANTIC STATUS LABELS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    ("Badge component system",              "badge-v" in h and "badge-p" in h),
    ("Verified badges used",                "VERIFIED" in h),
    ("Pending badges used",                 "NOT VERIFIED" in h),

    # â”€â”€ SAFETY BOUNDARY â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    ("Safety boundary visible",             "SOFTWARE SIMULATION" in h),
    ("Physical vehicle NO",                 "Physical vehicle" in h),
    ("External CAN NO",                     "External CAN" in h),
    ("Direct actuation NO",                 "Direct actuation" in h),
    ("No real emergency dispatch",          "Real emergency dispatch" in h or "real emergency" in h.lower()),

    # â”€â”€ HONEST SNAPDRAGON STATUS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    ("Snapdragon pending pill",             "SNAPDRAGON PENDING" in h),
    ("QNN not verified",                    "QNN" in h and "NOT VERIFIED" in h),
    ("Hardware measurement pending",        "Power Measurement" in h and "Thermal Measurement" in h and "NOT VERIFIED" in h),
    ("No fabricated NPU metrics",           "NPU ACTIVE" not in h),
    ("Snapdragon-aligned language",         "Snapdragon" in h),

    # â”€â”€ API CONTRACTS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    ("Evidence API fetch",                  "/api/evidence" in h),
    ("loadEvidence JS function",            "function loadEvidence" in h),
    ("renderAll JS function",               "function renderAll" in h),
]

print("=" * 60)
print("EDGERESILIENCE â€” UX QUALITY AUDIT")
print("=" * 60)
fails = 0
for name, ok in checks:
    print(("PASS" if ok else "FAIL"), name)
    if not ok:
        fails += 1

print()
print("=" * 60)
print("PROTECTED ARTIFACT CHECKSUMS")
print("=" * 60)
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
print("=" * 60)
print("EVIDENCE DATA CHECK")
print("=" * 60)
ev = json.loads((ROOT/"data/evidence/v4_demo_scenario.json").read_text("utf-8"))
print("Cycles:", len(ev["cycles"]))
for c in ev["cycles"]:
    pred = c["prediction"]["predicted_future_degradation"]
    print(f"  {c['cycle_id']}  conn={c['connectivity_state']}  risk={c['risk']['predictive_risk_level']}  deg={pred:.4f}")

print()
print("=" * 60)
total = len(checks) + len(artifacts)
print(f"FINAL RESULT: {'ALL PASS' if fails == 0 else str(fails) + ' FAILURES'} ({total - fails}/{total} checks)")
print("=" * 60)
print("Launch: python src/dashboard/server.py")
print("Open  : http://127.0.0.1:8765")

sys.exit(0 if fails == 0 else 1)


