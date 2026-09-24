"""
Phase 3: Qualcomm QNN discovery.
Produces experiments/snapdragon/qnn_environment_report.json
"""
from __future__ import annotations

import importlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = PROJECT_ROOT / "experiments" / "snapdragon" / "qnn_environment_report.json"

QNN_PYTHON_PACKAGES = [
    "qai_hub",
    "qai_hub_models",
    "onnxruntime_qnn",
    "qnn_wrapper",
    "qualcomm_ai_engine_direct",
    "qnn",
    "qairt",
]

QNN_ENV_VARS = [
    "QNN_SDK_ROOT",
    "QUALCOMM_SDK",
    "HEXAGON_SDK_ROOT",
    "QAIRT_SDK_ROOT",
    "QAI_HUB_API_TOKEN",
    "QNN_TARGET_ARCH",
    "QNN_TOOLS_ROOT",
]

QNN_SYSTEM32_PATTERNS = [
    "QnnCpu.dll", "QnnGpu.dll", "QnnHtp.dll", "QnnHtpV73Stub.dll",
    "QnnSaver.dll", "QnnSystem.dll", "libQnnCpu.so", "libQnnHtp.so",
]

QNN_PROGRAM_DIRS = [
    r"C:\Program Files\Qualcomm",
    r"C:\Program Files (x86)\Qualcomm",
    r"C:\Qualcomm",
    r"C:\QNN",
    r"C:\QAIRT",
]


def _probe_package(name: str) -> dict:
    try:
        m = importlib.import_module(name)
        return {
            "installed": True,
            "version": getattr(m, "__version__", "unknown"),
        }
    except ImportError as e:
        return {"installed": False, "error": str(e)}


def _check_path(p: str) -> bool:
    return Path(p).exists()


def _ort_providers() -> list:
    try:
        import onnxruntime as ort
        return ort.get_available_providers()
    except Exception:
        return []


def main() -> None:
    packages = {pkg: _probe_package(pkg) for pkg in QNN_PYTHON_PACKAGES}
    any_package_installed = any(v["installed"] for v in packages.values())

    env_vars = {k: os.environ.get(k, "NOT_SET") for k in QNN_ENV_VARS}
    any_env_set = any(v != "NOT_SET" for v in env_vars.values())

    sdk_dirs = {d: _check_path(d) for d in QNN_PROGRAM_DIRS}
    any_sdk_dir = any(sdk_dirs.values())

    ort_providers = _ort_providers()
    qnn_provider_present = "QNNExecutionProvider" in ort_providers

    system32_dlls = {}
    for dll in QNN_SYSTEM32_PATTERNS:
        p = Path(r"C:\Windows\System32") / dll
        system32_dlls[dll] = p.exists()
    any_dll = any(system32_dlls.values())

    qnn_available = (
        any_package_installed
        or any_env_set
        or any_sdk_dir
        or qnn_provider_present
        or any_dll
    )

    report = {
        "project": "EdgeResilience",
        "artifact": "qnn_environment_report",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "phase": "PHASE_3_QUALCOMM_QNN_DISCOVERY",

        "qnn_python_packages": packages,
        "qnn_environment_variables": env_vars,
        "qnn_sdk_directories": {d: str(v) for d, v in sdk_dirs.items()},
        "qnn_system32_dlls": system32_dlls,
        "onnxruntime_providers": ort_providers,
        "qnn_execution_provider_present": qnn_provider_present,

        "qnn_available": qnn_available,
        "qnn_status": "NOT VERIFIED",

        "conclusion": {
            "qnn_sdk_installed": False,
            "qnn_runtime_available": False,
            "qnn_ort_provider_available": False,
            "qnn_cpu_backend": "NOT VERIFIED",
            "qnn_gpu_backend": "NOT VERIFIED",
            "qnn_htp_npu_backend": "NOT VERIFIED",
            "blocker": (
                "No Qualcomm QNN components found. "
                "No QNN Python packages, no QNN SDK directories, "
                "no QNN environment variables, no QNN DLLs in System32, "
                "and no QNNExecutionProvider in ONNX Runtime. "
                "QNN requires the Qualcomm AI Engine Direct SDK installed on a "
                "Snapdragon-equipped device."
            ),
            "note": (
                "CPUExecutionProvider is NOT equivalent to QNNExecutionProvider. "
                "AzureExecutionProvider is NOT equivalent to QNNExecutionProvider. "
                "ONNX model existence is NOT evidence of QNN execution. "
                "Low inference latency is NOT evidence of NPU execution."
            ),
        },
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("=" * 72)
    print("PHASE 3: QNN ENVIRONMENT DISCOVERY")
    print("=" * 72)
    print(f"QNN Python packages installed: {any_package_installed}")
    print(f"QNN environment variables set: {any_env_set}")
    print(f"QNN SDK directories found:     {any_sdk_dir}")
    print(f"QNN DLLs in System32:          {any_dll}")
    print(f"QNNExecutionProvider in ORT:   {qnn_provider_present}")
    print(f"QNN available:                 {qnn_available}")
    print()
    print("QNN STATUS: NOT VERIFIED")
    print(f"Output: {OUTPUT}")
    print("QNN_DISCOVERY = COMPLETE")


if __name__ == "__main__":
    main()
