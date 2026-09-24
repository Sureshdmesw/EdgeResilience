# EdgeResilience — Snapdragon Environment Discovery

**Phase:** PHASE_1_HARDWARE_AND_ENVIRONMENT_DISCOVERY
**Status:** COMPLETE
**Generated:** See experiments/snapdragon/environment_report.json

---

## Hardware Inventory

| Field | Value | Verification Method | Verified |
|---|---|---|---|
| OS | Windows 10 (10.0.26200) | platform.system() / platform.release() | YES |
| Architecture | AMD64 | platform.machine() | YES |
| CPU | 12th Gen Intel Core i5-1235U | Get-CimInstance Win32_Processor | YES |
| CPU Manufacturer | GenuineIntel | Get-CimInstance Win32_Processor | YES |
| CPU Cores | 10 physical / 12 logical | Get-CimInstance Win32_Processor | YES |
| GPU | Intel UHD Graphics | Get-CimInstance Win32_VideoController | YES |
| GPU Driver | 32.0.101.7082 | Get-CimInstance Win32_VideoController | YES |
| System | Lenovo IdeaPad 3 15IAU7 (82RK) | Get-CimInstance Win32_ComputerSystem | YES |
| Snapdragon SoC | NOT PRESENT | PnP device scan | YES |
| Qualcomm hardware | NOT PRESENT | PnP device scan + DriverStore scan | YES |
| Hexagon DSP/NPU | NOT PRESENT | PnP device scan | YES |

---

## Software Environment

| Package | Version | Verified |
|---|---|---|
| Python | 3.11.9 | YES |
| PyTorch | 2.12.1+cpu | YES |
| ONNX | 1.23.0 | YES |
| ONNX Runtime | 1.30.0 | YES |
| NumPy | 2.4.6 | YES |
| scikit-learn | 1.9.0 | YES |

---

## ONNX Runtime Execution Providers

| Provider | Present |
|---|---|
| CPUExecutionProvider | YES |
| AzureExecutionProvider | YES |
| QNNExecutionProvider | NO |
| CUDAExecutionProvider | NO |
| DmlExecutionProvider | NO |

---

## Qualcomm / Snapdragon Discovery

| Check | Result | Method |
|---|---|---|
| Qualcomm PnP devices | NONE FOUND | Get-PnpDevice filter Qualcomm/Snapdragon/NPU/Hexagon/QNN |
| Qualcomm drivers in DriverStore | NONE FOUND | Get-ChildItem DriverStore\FileRepository |
| Qualcomm DLLs in System32 | NONE FOUND | Get-ChildItem System32 filter qualcomm/qnn/hexagon |
| QNN SDK directories | NONE FOUND | Check C:\Program Files\Qualcomm, C:\QNN, C:\QAIRT |
| QNN environment variables | NONE SET | Env var scan for QNN/QUALCOMM/SNAPDRAGON/HEXAGON/QAIRT |
| QNN PATH entries | NONE | PATH split and filter |
| qai_hub Python package | NOT INSTALLED | importlib probe |
| onnxruntime_qnn Python package | NOT INSTALLED | importlib probe |
| qualcomm_ai_engine_direct | NOT INSTALLED | importlib probe |

---

## Phase 2: Target Platform Identification

**Snapdragon hardware detected:** NO

This machine is a **Lenovo IdeaPad 3 15IAU7** with a **12th Gen Intel Core i5-1235U** processor.

- No Qualcomm SoC
- No Snapdragon chipset
- No Hexagon DSP or NPU
- No Qualcomm drivers
- No QNN SDK

**Snapdragon hardware: NOT AVAILABLE IN CURRENT ENVIRONMENT**

---

## Deployment Blocker

Snapdragon deployment requires:

1. A device with a Qualcomm Snapdragon SoC (e.g., Snapdragon X Elite, Snapdragon 8cx Gen 3, or equivalent)
2. Qualcomm AI Engine Direct SDK (QNN SDK) >= 2.x installed
3. `onnxruntime-qnn` or ONNX Runtime built with `QNNExecutionProvider`
4. Windows on ARM64 or Android target environment

**Current machine does not meet any of these requirements.**

---

## Evidence Artifact

`experiments/snapdragon/environment_report.json`
