from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

checks = []
failures = []


def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    checks.append((status, name, detail))
    if not condition:
        failures.append(name)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def exists(rel):
    return (ROOT / rel).is_file()


def load_json(rel):
    path = ROOT / rel
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception:
        return None


print("=" * 64)
print("EDGERESILIENCE SUBMISSION VALIDATION")
print("=" * 64)
print()

# ------------------------------------------------------------------
# Core validated EdgeResilience artifacts
# ------------------------------------------------------------------

core_artifacts = {
    "V4 model":
        "models/edgeresilience/temporal_predictor_v4.pt",

    "V4 dataset":
        "data/processed/temporal/edgeresilience_temporal_dataset_v4.jsonl",

    "Static ONNX":
        "models/edgeresilience/temporal_predictor_v4.onnx",

    "Dynamic ONNX":
        "models/edgeresilience/temporal_predictor_v4_dynamic.onnx",

    "V4 inference engine":
        "src/ai/v4_inference.py",

    "V4 runtime":
        "src/resilience/v4_runtime.py",

    "V4 risk policy":
        "src/resilience/v4_risk.py",

    "Demo evidence":
        "data/evidence/v4_demo_scenario.json",

    "Dashboard generator":
        "src/dashboard/generate_dashboard.py",

    "Dashboard audit":
        "src/dashboard/audit.py",

    "UX audit":
        "src/dashboard/ux_audit.py",
}

print("[CORE ARTIFACTS]")

for name, rel in core_artifacts.items():
    check(name, exists(rel), rel)
    if exists(rel):
        print(f"PASS {name}: {rel}")
    else:
        print(f"FAIL {name}: {rel}")

print()

# ------------------------------------------------------------------
# Snapdragon deployment artifacts
# ------------------------------------------------------------------

snapdragon_artifacts = {
    "AI Hub single-file ONNX":
        "models/edgeresilience/snapdragon/temporal_predictor_v4_aihub.onnx",

    "QNN-ready ONNX":
        "models/edgeresilience/snapdragon/temporal_predictor_v4_qnn_ready.onnx",

    "Snapdragon validation matrix":
        "experiments/snapdragon/snapdragon_validation_matrix.json",

    "Encoder Block 1 HTP profile":
        "experiments/snapdragon/v4_encoder_block1_htp_profile.json",

    "Encoder Block 2 HTP profile":
        "experiments/snapdragon/v4_encoder_block2_htp_profile.json",

    "Snapdragon validation documentation":
        "docs/snapdragon/SNAPDRAGON_VALIDATION.md",

    "Deployment implementation":
        "src/snapdragon/deployment.py",

    "Deployment manifest":
        "experiments/snapdragon_deployment_manifest_v4.json",
}

print("[SNAPDRAGON ARTIFACTS]")

for name, rel in snapdragon_artifacts.items():
    check(name, exists(rel), rel)
    if exists(rel):
        print(f"PASS {name}: {rel}")
    else:
        print(f"FAIL {name}: {rel}")

print()

# ------------------------------------------------------------------
# Snapdragon validation matrix semantics
# ------------------------------------------------------------------

matrix = load_json("experiments/snapdragon/snapdragon_validation_matrix.json")

print("[SNAPDRAGON STATUS]")

if matrix is None:
    check(
        "Validation matrix readable",
        False,
        "experiments/snapdragon/snapdragon_validation_matrix.json",
    )
    print("FAIL Validation matrix readable")
else:
    check("Validation matrix readable", True)
    print("PASS Validation matrix readable")

    status = matrix.get("status", "")
    full_model = matrix.get("full_model", {})
    components = matrix.get("components", [])

    check(
        "Component-level Snapdragon validation recorded",
        "COMPONENT_LEVEL" in status,
        status,
    )

    check(
        "Full-model HTP not verified",
        "HTP_NOT_VERIFIED" in status,
        status,
    )

    print(f"Status: {status}")

    full_compile = (
        full_model.get("compile_status") == "VERIFIED"
        if isinstance(full_model, dict)
        else False
    )

    full_htp = (
        full_model.get("htp_profile_status") == "VERIFIED"
        if isinstance(full_model, dict)
        else False
    )

    check(
        "Full V4 compilation verified",
        full_compile is True,
    )

    check(
        "Full V4 HTP remains unverified",
        full_htp is False,
    )

    print(f"Full V4 compile verified: {full_compile}")
    print(f"Full V4 HTP verified:     {full_htp}")

    exact_component_names = {
        "Encoder Block 1",
        "Encoder Block 2",
        "Temporal pooling",
    }

    found_names = set()

    for component in components:
        if isinstance(component, dict):
            name = component.get("name", "")
            if name in exact_component_names:
                found_names.add(name)

    for name in sorted(exact_component_names):
        check(
            f"{name} evidence present",
            name in found_names,
        )

print()

# ------------------------------------------------------------------
# Safety boundary
# ------------------------------------------------------------------

print("[SAFETY BOUNDARY]")

demo = load_json("data/evidence/v4_demo_scenario.json")

if demo is None:
    check("Demo evidence readable", False)
    print("FAIL Demo evidence readable")
else:
    check("Demo evidence readable", True)
    print("PASS Demo evidence readable")

    boundary = demo.get("safety_boundary", {})

    expected_false = {
        "physical_vehicle": False,
        "external_can_transmission": False,
        "direct_actuation": False,
        "production_vehicle_connection": False,
    }

    for key, expected in expected_false.items():
        actual = boundary.get(key)
        check(
            f"{key} is false",
            actual is expected,
            f"actual={actual}",
        )
        print(f"{'PASS' if actual is expected else 'FAIL'} {key}: {actual}")

print()

# ------------------------------------------------------------------
# Protected checksums
# ------------------------------------------------------------------

print("[PROTECTED CHECKSUMS]")

expected_hashes = {
    "V4 model":
        (
            "models/edgeresilience/temporal_predictor_v4.pt",
            "b551ad9f02b56668ef3f8f7873133748275307f1934ec7fd77da14e7325d26b9",
        ),

    "V4 dataset":
        (
            "data/processed/temporal/edgeresilience_temporal_dataset_v4.jsonl",
            "02a82f0f5ee78dc4e3be28b81b53b6eb4eb884600a4734f3eb3aaa279cb3a911",
        ),

    "Dynamic ONNX":
        (
            "models/edgeresilience/temporal_predictor_v4_dynamic.onnx",
            "ACB43A20C9FA64577C56BDFE3AA3C2EA96B6691420C0A7994DC5FD9F230C0E5D",
        ),
}

for name, (rel, expected) in expected_hashes.items():
    path = ROOT / rel

    if not path.is_file():
        check(f"{name} checksum", False, "file missing")
        print(f"FAIL {name}: file missing")
        continue

    actual = sha256(path)
    ok = actual.lower() == expected.lower()

    check(f"{name} checksum", ok, actual)

    print(f"{'PASS' if ok else 'FAIL'} {name}")
    print(f"      {actual}")

print()

# ------------------------------------------------------------------
# Dashboard validation
# ------------------------------------------------------------------

print("[DASHBOARD VALIDATION]")

audit_script = ROOT / "src/dashboard/audit.py"
ux_script = ROOT / "src/dashboard/ux_audit.py"

check("Dashboard audit script exists", audit_script.is_file())
check("UX audit script exists", ux_script.is_file())

dashboard_parts = [
    "src/dashboard/_part1_head.html",
    "src/dashboard/_part2_body.html",
    "src/dashboard/_part3_pages.html",
]

for rel in dashboard_parts:
    check(f"Dashboard artifact: {Path(rel).name}", exists(rel))

print("Dashboard checks are represented by the dedicated audit scripts.")
print("Run:")
print("  python .\\src\\dashboard\\audit.py")
print("  python .\\src\\dashboard\\ux_audit.py")

print()

# ------------------------------------------------------------------
# Final result
# ------------------------------------------------------------------

print("=" * 64)

if failures:
    print(f"FINAL RESULT: {len(failures)} FAILURES")
    print()
    for failure in failures:
        print(f"FAIL: {failure}")
    sys.exit(1)

print("FINAL RESULT: ALL REQUIRED CHECKS PASSED")
print("=" * 64)

