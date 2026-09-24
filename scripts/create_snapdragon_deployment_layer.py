from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

code = r'''
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional
import json


@dataclass(frozen=True)
class SnapdragonRuntimeConfig:
    """
    Deployment configuration for EdgeResilience edge inference.

    This abstraction does not claim that a Snapdragon backend is available
    or verified. Hardware/backend verification must be established by an
    actual deployment experiment.
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

    Values are only valid when populated by an actual benchmark.
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
    Records the intended edge deployment configuration and its
    verification status.
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
                "verified": False,
            },
            {
                "name": "qualcomm_qnn",
                "verified": False,
            },
        ]

        self.snapdragon_hardware = {
            "verified": False,
            "device": None,
            "soc": None,
            "accelerator": None,
            "sdk": None,
        }

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
            "status": "PLANNED_EDGE_DEPLOYMENT",
        }

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(
            json.dumps(
                self.to_dict(),
                indent=2,
            ),
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
    print("SNAPDRAGON_HARDWARE_VERIFIED = FALSE")


if __name__ == "__main__":
    create_v4_manifest(ROOT)
'''

target = ROOT / "src" / "snapdragon" / "deployment.py"
target.write_text(code, encoding="utf-8")

print(f"Created: {target}")
