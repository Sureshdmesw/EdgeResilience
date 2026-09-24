from __future__ import annotations

import hashlib
import platform
import time
from dataclasses import asdict, dataclass
from typing import Any, Callable, Sequence


@dataclass(frozen=True)
class InferenceRequest:
    """
    Input to the edge inference runtime.

    The runtime receives an already prepared model input.
    Vehicle actuation and external CAN communication are outside
    this interface.
    """

    model_name: str
    model_source: str
    input_shape: tuple[int, ...]
    input_data: Any


@dataclass(frozen=True)
class InferenceMeasurement:
    """
    Measurement captured for one inference operation.

    These values describe the software runtime that was actually
    used. They must not be interpreted as Snapdragon-specific
    measurements unless the runtime reports a verified Snapdragon
    environment.
    """

    runtime_name: str
    execution_provider: str
    device: str
    latency_ms: float
    input_shape: tuple[int, ...]
    model_name: str
    model_source: str


@dataclass(frozen=True)
class EdgeInferenceResult:
    """
    Result of one edge inference operation.
    """

    output: Any
    measurement: InferenceMeasurement

    def to_dict(self) -> dict[str, Any]:
        return {
            "output": self.output,
            "measurement": asdict(
                self.measurement
            ),
        }


class EdgeInferenceRuntime:
    """
    Runtime abstraction for EdgeResilience inference.

    This class deliberately separates model execution from the
    resilience pipeline so that CPU reference measurements and
    future Snapdragon measurements can be compared without
    changing the higher-level safety logic.

    Safety boundary:
        - no vehicle actuation
        - no external CAN transmission
        - no production vehicle connection
        - software inference only
    """

    def __init__(
        self,
        *,
        runtime_name: str = "python_reference",
        execution_provider: str = "CPU",
        device: str = "CPU",
    ) -> None:
        self.runtime_name = runtime_name
        self.execution_provider = execution_provider
        self.device = device

    def infer(
        self,
        request: InferenceRequest,
        inference_fn: Callable[[Any], Any],
    ) -> EdgeInferenceResult:
        """
        Execute one inference operation and measure wall-clock
        latency.

        inference_fn is supplied by the caller so this runtime
        remains independent of a specific ML framework.
        """

        start_ns = time.perf_counter_ns()

        output = inference_fn(
            request.input_data
        )

        elapsed_ns = (
            time.perf_counter_ns()
            - start_ns
        )

        latency_ms = elapsed_ns / 1_000_000.0

        measurement = InferenceMeasurement(
            runtime_name=self.runtime_name,
            execution_provider=(
                self.execution_provider
            ),
            device=self.device,
            latency_ms=latency_ms,
            input_shape=request.input_shape,
            model_name=request.model_name,
            model_source=request.model_source,
        )

        return EdgeInferenceResult(
            output=output,
            measurement=measurement,
        )

    def environment(self) -> dict[str, str]:
        """
        Return basic runtime environment information.
        """

        return {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "runtime_name": self.runtime_name,
            "execution_provider": (
                self.execution_provider
            ),
            "device": self.device,
        }


def sha256_bytes(data: bytes) -> str:
    """
    Calculate SHA-256 for an artifact or serialized model payload.
    """

    return hashlib.sha256(data).hexdigest()


def summarize_latencies(
    measurements: Sequence[InferenceMeasurement],
) -> dict[str, float]:
    """
    Produce simple latency statistics.

    Returns an empty dictionary when no measurements exist.
    """

    if not measurements:
        return {}

    values = sorted(
        float(m.latency_ms)
        for m in measurements
    )

    count = len(values)

    mean_ms = (
        sum(values) / count
    )

    median_index = count // 2

    if count % 2:
        median_ms = values[
            median_index
        ]
    else:
        median_ms = (
            values[median_index - 1]
            + values[median_index]
        ) / 2.0

    return {
        "count": float(count),
        "min_ms": values[0],
        "mean_ms": mean_ms,
        "median_ms": median_ms,
        "max_ms": values[-1],
    }