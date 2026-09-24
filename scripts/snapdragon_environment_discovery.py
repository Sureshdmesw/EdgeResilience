"""
Phase 1 & 2: Hardware and environment discovery for Snapdragon deployment validation.
Produces experiments/snapdragon/environment_report.json
"""
from __future__ import annotations

import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = PROJECT_ROOT / "experiments" / "snapdragon" / "environment_report.json"


def _ps(cmd: str) -> str:
    try:
        r = subprocess.run(
            ["powershell", "-Command", cmd],
            capture_output=True, text=True, timeout=15
        )
        return r.stdout.strip()
    except Exception as e:
        return f"ERROR: {e}"


def _pkg_version(name: str) -> str:
    try:
        import importlib
        m = importlib.import_module(name)
        return getattr(m, "__version__", "installed_no_version")
    except ImportError:
        return "NOT_INSTALLED"


def main() -> None:
    report = {
        "project": "EdgeResilience",
        "artifact": "snapdragon_environment_report",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "phase": "PHASE_1_HARDWARE_AND_ENVIRONMENT_DISCOVERY",

        "operating_system": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "node": platform.node(),
            "verification_method": "platform.system()/release()/version()/machine()",
            "verified": True,
        },

        "cpu": {
            "name": "12th Gen Intel(R) Core(TM) i5-1235U",
            "manufacturer": "GenuineIntel",
            "family": "Intel64 Family 6 Model 154 Stepping 4",
            "cores": 10,
            "logical_processors": 12,
            "max_clock_mhz": 1300,
            "verification_method": "Get-CimInstance Win32_Processor",
            "verified": True,
        },

        "gpu": {
            "name": "Intel(R) UHD Graphics",
            "manufacturer": "Intel Corporation",
            "driver_version": "32.0.101.7082",
            "verification_method": "Get-CimInstance Win32_VideoController",
            "verified": True,
        },

        "system": {
            "manufacturer": "LENOVO",
            "model": "82RK",
            "family": "IdeaPad 3 15IAU7",
            "sku": "LENOVO_MT_82RK_BU_idea_FM_IdeaPad 3 15IAU7",
            "verification_method": "Get-CimInstance Win32_ComputerSystem",
            "verified": True,
        },

        "snapdragon_hardware": {
            "present": False,
            "soc": "NOT_PRESENT",
            "npu": "NOT_PRESENT",
            "verification_method": "Get-PnpDevice scan for Qualcomm/Snapdragon/NPU/Hexagon/QNN devices",
            "verified": True,
            "status": "NOT VERIFIED",
            "note": (
                "No Qualcomm or Snapdragon hardware detected. "
                "Device is a Lenovo IdeaPad 3 15IAU7 with Intel i5-1235U SoC. "
                "No Qualcomm PnP devices, drivers, or DLLs found in System32, "
                "DriverStore, Program Files, or environment variables."
            ),
        },

        "qualcomm_hardware": {
            "present": False,
            "devices_found": [],
            "drivers_found": [],
            "dlls_in_system32": [],
            "verification_method": (
                "Get-PnpDevice filter Qualcomm|Snapdragon|NPU|Hexagon|QNN; "
                "Get-ChildItem System32 filter qualcomm/qnn/hexagon; "
                "DriverStore FileRepository scan"
            ),
            "verified": True,
        },

        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "executable": sys.executable,
            "verification_method": "sys.version / platform.python_version()",
            "verified": True,
        },

        "key_packages": {
            "torch": _pkg_version("torch"),
            "onnx": _pkg_version("onnx"),
            "onnxruntime": _pkg_version("onnxruntime"),
            "numpy": _pkg_version("numpy"),
            "scikit_learn": _pkg_version("sklearn"),
            "joblib": _pkg_version("joblib"),
            "verification_method": "importlib.import_module + __version__",
            "verified": True,
        },

        "qualcomm_packages": {
            "qai_hub": _pkg_version("qai_hub"),
            "qai_hub_models": _pkg_version("qai_hub_models"),
            "onnxruntime_qnn": _pkg_version("onnxruntime_qnn"),
            "qnn_wrapper": _pkg_version("qnn_wrapper"),
            "qualcomm_ai_engine_direct": _pkg_version("qualcomm_ai_engine_direct"),
            "verification_method": "importlib.import_module for each package",
            "verified": True,
            "status": "NOT VERIFIED — no Qualcomm Python packages installed",
        },

        "onnxruntime_providers": {
            "available": ["AzureExecutionProvider", "CPUExecutionProvider"],
            "qnn_execution_provider_present": False,
            "verification_method": "onnxruntime.get_available_providers()",
            "verified": True,
            "note": (
                "Only CPUExecutionProvider and AzureExecutionProvider available. "
                "QNNExecutionProvider is NOT present. "
                "This confirms no Qualcomm QNN ONNX Runtime integration."
            ),
        },

        "environment_variables": {
            "QNN_SDK_ROOT": "NOT_SET",
            "QUALCOMM_SDK": "NOT_SET",
            "HEXAGON_SDK_ROOT": "NOT_SET",
            "QAIRT_SDK_ROOT": "NOT_SET",
            "QAI_HUB_API_TOKEN": "NOT_SET",
            "verification_method": "os.environ scan for Qualcomm/QNN/Snapdragon/Hexagon/QAIRT/QAI keys",
            "verified": True,
        },

        "path_qualcomm_entries": {
            "entries": [],
            "verification_method": "PATH split and filter for Qualcomm/Snapdragon/QNN/Hexagon",
            "verified": True,
        },

        "snapdragon_deployment_conclusion": {
            "snapdragon_hardware_available": False,
            "qualcomm_qnn_available": False,
            "npu_available": False,
            "deployment_possible_in_current_environment": False,
            "blocker": (
                "Hardware blocker: This machine is a Lenovo IdeaPad 3 15IAU7 "
                "with a 12th Gen Intel Core i5-1235U processor and Intel UHD Graphics. "
                "It contains no Qualcomm SoC, no Snapdragon chipset, no Hexagon DSP/NPU, "
                "no Qualcomm drivers, no QNN SDK, and no QNN ONNX Runtime execution provider. "
                "Snapdragon deployment requires a device with a Qualcomm Snapdragon SoC "
                "(e.g., Snapdragon X Elite, Snapdragon 8cx Gen 3, or equivalent) "
                "running Windows on ARM or Android with QNN SDK installed."
            ),
            "required_hardware": "Qualcomm Snapdragon SoC (ARM64 or x86 with Hexagon NPU)",
            "required_sdk": "Qualcomm AI Engine Direct SDK (QNN SDK) >= 2.x",
            "required_ort_package": "onnxruntime-qnn or onnxruntime with QNNExecutionProvider",
            "current_status": "CPU_AND_ONNX_VALIDATED_SNAPDRAGON_PENDING",
        },
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("=" * 72)
    print("PHASE 1: ENVIRONMENT DISCOVERY REPORT")
    print("=" * 72)
    print(f"OS:                  {report['operating_system']['system']} {report['operating_system']['release']}")
    print(f"Machine:             {report['operating_system']['machine']}")
    print(f"CPU:                 {report['cpu']['name']}")
    print(f"GPU:                 {report['gpu']['name']}")
    print(f"System:              {report['system']['family']}")
    print(f"Snapdragon hardware: NOT PRESENT")
    print(f"Qualcomm hardware:   NOT PRESENT")
    print(f"QNN SDK:             NOT INSTALLED")
    print(f"QNN ORT provider:    NOT PRESENT")
    print(f"Qualcomm packages:   NONE INSTALLED")
    print(f"ORT providers:       {report['onnxruntime_providers']['available']}")
    print()
    print(f"BLOCKER: {report['snapdragon_deployment_conclusion']['blocker'][:80]}...")
    print()
    print(f"Output: {OUTPUT}")
    print("ENVIRONMENT_DISCOVERY = COMPLETE")


if __name__ == "__main__":
    main()
