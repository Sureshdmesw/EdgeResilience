from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional
import json


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class SnapdragonRuntimeConfig:
    """
    EdgeResilience Snapdragon deployment configuration.

    Status reflects measured evidence only. Component-level Snapdragon
    validation does not imply full-model HTP validation.
    """

    model_path: str
    backend: str = "cpu_reference"
    device: str = "reference_cpu"
    hardware_verified: bool = False
    accelerator_verified: bool = False


@dataclass
class SnapdragonBenchmarkResult:
    """
    Benchmark evidence container.

    Values are valid only when populated by an actual benchmark.
    """

    backend: str
    device: str
    hardware_verified: bool

    samples: int = 0
    warmup_runs: int = 0

    mean_latency_ms: Optional[float] = None
    median_latency_ms: Optional[float] = None
    p95_latency_ms: Optional[float] = None

    throughput_samples_per_second: Optional[float] = None
    peak_memory_mb: Optional[float] = None
    power_watts: Optional[float] = None
    energy_per_inference_mj: Optional[float] = None

    notes: str = ""

    def to_dict(self):
        return asdict(self)


class SnapdragonDeploymentManifest:
    """
    Records the current EdgeResilience deployment evidence.

    Important:
    - Snapdragon component validation is VERIFIED.
    - Full V4 QNN/HTP execution remains NOT VERIFIED.
    - Validation occurred on Qualcomm Snapdragon X Elite CRD.
    - This is not HP-branded hardware validation.
    """

    def __init__(
        self,
        model_path: str,
        model_format: str = "pytorch",
        input_shape=(1, 12, 17),
        output_shape=(1,),
    ):
        self.model_path = str(model_path)
        self.model_format = model_format
        self.input_shape = list(input_shape)
        self.output_shape = list(output_shape)

        self.backends = [
            {
                "name": "cpu_reference",
                "verified": True,
            },
            {
                "name": "onnx",
                "verified": True,
            },
            {
                "name": "qualcomm_qnn",
                "verified": True,
                "scope": "component_level",
                "full_model_verified": False,
            },
        ]

        self.snapdragon_hardware = {
            "verified": True,
            "scope": "component_level",
            "device": "Snapdragon X Elite CRD",
            "os": "Windows 11",
            "soc": "SC8380XP",
            "chipset": "qualcomm-snapdragon-x-elite",
            "accelerator": "Qualcomm QNN / HTP",
            "hexagon": "v73",
            "hp_branded_pc_verified": False,
        }

        self.full_model = {
            "compile_verified": True,
            "compile_job": "jgdd3v6zg",
            "htp_verified": False,
            "htp_profile_job": "j5wl79zmp",
            "htp_failure": "QNN graph finalization failed with error code 6000",
        }

        self.verified_components = [
            {
                "name": "Encoder Block 1",
                "htp_verified": True,
                "profile_job": "jp8ex8ekp",
                "inference_ms": 0.045,
                "npu_layers": 41,
            },
            {
                "name": "Encoder Block 2",
                "htp_verified": True,
                "profile_job": "j5qlywoep",
                "inference_ms": 0.042,
                "npu_layers": 40,
            },
            {
                "name": "Temporal Pooling",
                "htp_verified": True,
                "profile_job": "jp8ex6yqp",
                "inference_ms": 0.038,
                "load_ms": 493.242,
                "peak_memory_mib": 28.328125,
                "npu_layers": 24,
            },
            {
                "name": "Prediction Head",
                "htp_verified": True,
                "profile_job": "jgk24dlog",
            },
        ]

        self.status = (
            "SNAPDRAGON_COMPONENT_LEVEL_VALIDATED_FULL_MODEL_HTP_NOT_VERIFIED"
        )

    def to_dict(self):
        return {
            "project": "EdgeResilience",
            "artifact_type": "snapdragon_deployment_manifest",
            "model_path": self.model_path,
            "model_format": self.model_format,
            "input_shape": self.input_shape,
            "output_shape": self.output_shape,
            "backends": self.backends,
            "snapdragon_hardware": self.snapdragon_hardware,
            "full_model": self.full_model,
            "verified_components": self.verified_components,
            "status": self.status,
        }

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(
            json.dumps(self.to_dict(), indent=2),
            encoding="utf-8",
        )


def create_v4_manifest(root):
    model = (
        root
        / "models"
        / "edgeresilience"
        / "temporal_predictor_v4.pt"
    )

    manifest = SnapdragonDeploymentManifest(
        model_path=str(model.relative_to(root))
    )

    output = (
        root
        / "experiments"
        / "snapdragon_deployment_manifest_v4.json"
    )

    manifest.save(output)

    print(f"Created: {output}")
    print("SNAPDRAGON_DEPLOYMENT_MANIFEST = PASS")
    print("SNAPDRAGON_COMPONENT_LEVEL_VALIDATED = TRUE")
    print("SNAPDRAGON_FULL_MODEL_HTP_VERIFIED = FALSE")


if __name__ == "__main__":
    create_v4_manifest(ROOT)
