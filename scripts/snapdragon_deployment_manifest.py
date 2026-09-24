"""
Phase 11: Snapdragon deployment manifest.
Produces experiments/snapdragon/snapdragon_deployment_manifest.json
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(r"E:\EdgeResilience")
OUTPUT = PROJECT_ROOT / "experiments" / "snapdragon" / "snapdragon_deployment_manifest.json"

CHECKPOINT = PROJECT_ROOT / "models" / "edgeresilience" / "temporal_predictor_v4.pt"
SRC_ONNX = PROJECT_ROOT / "models" / "edgeresilience" / "temporal_predictor_v4_dynamic.onnx"
DERIVATIVE = PROJECT_ROOT / "models" / "edgeresilience" / "snapdragon" / "temporal_predictor_v4_qnn_ready.onnx"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest().upper()


def main() -> None:
    ckpt_sha = sha256_file(CHECKPOINT)
    onnx_sha = sha256_file(SRC_ONNX)
    drv_sha = sha256_file(DERIVATIVE)

    manifest = {
        "project": "EdgeResilience",
        "artifact": "snapdragon_deployment_manifest",
        "generated_utc": datetime.now(timezone.utc).isoformat(),

        "model_name": "EdgeResilience_V4_TemporalPredictor",
        "source_checkpoint": "models/edgeresilience/temporal_predictor_v4.pt",
        "source_checkpoint_sha256": ckpt_sha,
        "source_checkpoint_integrity": (
            "PASS"
            if ckpt_sha == "B551AD9F02B56668EF3F8F7873133748275307F1934EC7FD77DA14E7325D26B9"
            else "FAIL"
        ),

        "source_onnx": "models/edgeresilience/temporal_predictor_v4_dynamic.onnx",
        "source_onnx_sha256": onnx_sha,
        "source_onnx_integrity": (
            "PASS"
            if onnx_sha == "ACB43A20C9FA64577C56BDFE3AA3C2EA96B6691420C0A7994DC5FD9F230C0E5D"
            else "FAIL"
        ),

        "derived_artifact": {
            "path": "models/edgeresilience/snapdragon/temporal_predictor_v4_qnn_ready.onnx",
            "sha256": drv_sha,
            "provenance": "ADAPTED from source ONNX via ORT_ENABLE_BASIC constant folding",
            "relationship": "ADAPTED",
            "mod_nodes_eliminated": True,
            "node_count": 176,
            "operators": [
                "Add", "Cast", "Concat", "Div", "Erf", "Gather", "Gemm",
                "LayerNormalization", "MatMul", "Mul", "ReduceSum", "Relu",
                "Reshape", "Shape", "Sigmoid", "Slice", "Softmax", "Sqrt",
                "Squeeze", "Transpose", "Unsqueeze",
            ],
            "numerical_equivalence_vs_source": {
                "samples": 200,
                "max_absolute_error": 0.0,
                "tolerance": 1e-5,
                "result": "PASS",
            },
            "onnx_checker": "PASS",
        },

        "hardware": {
            "snapdragon_present": False,
            "device": "NOT VERIFIED",
            "soc": "NOT VERIFIED",
            "cpu": "NOT VERIFIED",
            "gpu": "NOT VERIFIED",
            "npu": "NOT VERIFIED",
            "memory": "NOT VERIFIED",
            "os": "NOT VERIFIED",
        },

        "software_environment": {
            "driver_versions": "NOT VERIFIED",
            "qualcomm_runtime_version": "NOT VERIFIED",
            "qnn_version": "NOT VERIFIED",
            "onnxruntime_version": "NOT VERIFIED",
            "qnn_execution_provider": "NOT VERIFIED",
        },

        "backends": [
            {"name": "cpu_reference_pytorch", "verified": True,
             "throughput_samples_per_sec": 33800, "mean_latency_ms": 1.66},
            {"name": "onnx_cpu", "verified": True,
             "throughput_samples_per_sec": None,
             "mean_latency_ms": 0.28,
             "speedup_vs_pytorch": "~5.99x"},
            {"name": "qualcomm_qnn_cpu", "verified": False, "status": "NOT VERIFIED"},
            {"name": "qualcomm_qnn_gpu", "verified": False, "status": "NOT VERIFIED"},
            {"name": "qualcomm_qnn_htp_npu", "verified": False, "status": "NOT VERIFIED"},
        ],

        "input_shape": ["batch", 12, 17],
        "output_shape": ["batch"],
        "input_name": "vehicle_temporal_features",
        "output_name": "future_resilience_degradation",
        "opset": 17,

        "npu_status": "NOT VERIFIED",
        "qnn_conversion_status": "NOT PERFORMED — no QNN SDK present",
        "snapdragon_execution_status": "NOT PERFORMED — no Snapdragon hardware present",

        "numerical_equivalence": {
            "pytorch_vs_onnx_cpu": {
                "max_absolute_error": 5.96e-8,
                "result": "PASS",
                "source": "experiments/v4_dynamic_onnx_equivalence_report.json",
            },
            "onnx_cpu_vs_qnn_ready_derivative": {
                "max_absolute_error": 0.0,
                "result": "PASS",
                "source": "experiments/snapdragon/qnn_ready_model_report.json",
            },
            "qnn_execution_vs_reference": "NOT VERIFIED",
        },

        "performance": {
            "cpu_pytorch_mean_latency_ms": 1.66,
            "cpu_pytorch_median_latency_ms": 1.62,
            "cpu_pytorch_p95_latency_ms": 1.96,
            "onnx_cpu_mean_latency_ms": 0.28,
            "onnx_cpu_median_latency_ms": 0.28,
            "onnx_cpu_p95_latency_ms": 0.29,
            "snapdragon_cpu_latency_ms": "NOT VERIFIED",
            "snapdragon_gpu_latency_ms": "NOT VERIFIED",
            "snapdragon_npu_latency_ms": "NOT VERIFIED",
            "throughput_cpu_pytorch_samples_per_sec": 33800,
            "throughput_onnx_cpu_samples_per_sec": "NOT MEASURED",
            "throughput_snapdragon_samples_per_sec": "NOT VERIFIED",
        },

        "resource_measurements": {
            "model_size_onnx_bytes": SRC_ONNX.stat().st_size,
            "model_size_qnn_ready_bytes": DERIVATIVE.stat().st_size,
            "memory_footprint_mb": "NOT VERIFIED",
            "power_watts": "NOT VERIFIED",
            "thermal": "NOT VERIFIED",
            "runtime_init_time_ms": "NOT VERIFIED",
        },

        "validation_timestamp": datetime.now(timezone.utc).isoformat(),
        "overall_status": "CPU_AND_ONNX_VALIDATED_SNAPDRAGON_PENDING",

        "qnn_conversion_command": (
            "qnn-onnx-converter "
            "--input_network models/edgeresilience/snapdragon/temporal_predictor_v4_qnn_ready.onnx "
            "--output_path models/edgeresilience/snapdragon/temporal_predictor_v4.cpp "
            "--input_dim vehicle_temporal_features 1,12,17"
        ),

        "safety_boundary": {
            "test_type": "software_simulation",
            "physical_vehicle": False,
            "external_can_transmission": False,
            "direct_actuation": False,
            "production_vehicle_connection": False,
        },
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("=" * 72)
    print("PHASE 11: SNAPDRAGON DEPLOYMENT MANIFEST")
    print("=" * 72)
    print(f"Checkpoint integrity:  {manifest['source_checkpoint_integrity']}")
    print(f"Source ONNX integrity: {manifest['source_onnx_integrity']}")
    print(f"Derivative SHA256:     {drv_sha}")
    print(f"Derivative equiv:      PASS (max_err=0.0)")
    print(f"Snapdragon hardware:   NOT VERIFIED")
    print(f"QNN:                   NOT VERIFIED")
    print(f"NPU:                   NOT VERIFIED")
    print(f"Overall status:        CPU_AND_ONNX_VALIDATED_SNAPDRAGON_PENDING")
    print(f"Output: {OUTPUT}")
    print("SNAPDRAGON_DEPLOYMENT_MANIFEST = COMPLETE")


if __name__ == "__main__":
    main()
