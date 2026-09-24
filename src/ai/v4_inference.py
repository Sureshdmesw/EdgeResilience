from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import torch

from src.ai.temporal_predictor import (
    EdgeResilienceTemporalPredictor,
    TemporalModelConfig,
)


@dataclass(frozen=True)
class V4PredictionResult:
    predicted_future_degradation: float
    model_name: str
    model_source: str
    feature_count: int
    observation_steps: int


class V4InferenceEngine:
    """
    EdgeResilience V4 temporal inference adapter.

    Input:
        12 sequential observations containing the checkpoint's
        exact 17-feature contract.

    Output:
        Predicted future resilience degradation.

    This adapter does not transmit CAN data, actuate a vehicle,
    connect to a production vehicle, or perform physical testing.
    """

    def __init__(
        self,
        checkpoint_path: str | Path,
        device: str = "cpu",
    ) -> None:
        self.checkpoint_path = Path(checkpoint_path)
        self.device = torch.device(device)

        checkpoint = torch.load(
            self.checkpoint_path,
            map_location=self.device,
            weights_only=False,
        )

        config_data = checkpoint["config"]

        config = TemporalModelConfig(
            input_features=int(config_data["input_features"]),
            sequence_length=int(config_data["sequence_length"]),
            d_model=int(config_data["d_model"]),
            nhead=int(config_data["nhead"]),
            num_layers=int(config_data["num_layers"]),
            dim_feedforward=int(
                config_data["dim_feedforward"]
            ),
            dropout=float(config_data["dropout"]),
        )

        self.feature_names = list(
            checkpoint["feature_names"]
        )

        self.normalization_mean = torch.tensor(
            checkpoint["normalization_mean"],
            dtype=torch.float32,
            device=self.device,
        )

        self.normalization_std = torch.tensor(
            checkpoint["normalization_std"],
            dtype=torch.float32,
            device=self.device,
        )

        if len(self.feature_names) != config.input_features:
            raise ValueError(
                "Feature-name count does not match model input size."
            )

        if len(self.normalization_mean) != config.input_features:
            raise ValueError(
                "Normalization mean does not match model input size."
            )

        if len(self.normalization_std) != config.input_features:
            raise ValueError(
                "Normalization std does not match model input size."
            )

        if torch.any(self.normalization_std <= 0):
            raise ValueError(
                "Normalization standard deviation contains "
                "non-positive values."
            )

        self.model = EdgeResilienceTemporalPredictor(
            config=config
        )

        self.model.load_state_dict(
            checkpoint["model_state_dict"]
        )

        self.model.to(self.device)
        self.model.eval()

        self.config = config

    def _build_tensor(
        self,
        observations: Sequence[Mapping[str, Any]],
    ) -> torch.Tensor:

        if len(observations) != self.config.sequence_length:
            raise ValueError(
                f"Expected {self.config.sequence_length} "
                f"observations, got {len(observations)}."
            )

        rows = []

        for index, observation in enumerate(observations):
            missing = [
                name
                for name in self.feature_names
                if name not in observation
            ]

            if missing:
                raise ValueError(
                    f"Observation {index} is missing features: "
                    f"{missing}"
                )

            rows.append([
                float(observation[name])
                for name in self.feature_names
            ])

        tensor = torch.tensor(
            rows,
            dtype=torch.float32,
            device=self.device,
        ).unsqueeze(0)

        normalized = (
            tensor - self.normalization_mean
        ) / self.normalization_std

        return normalized

    @torch.no_grad()
    def predict(
        self,
        observations: Sequence[Mapping[str, Any]],
    ) -> V4PredictionResult:

        x = self._build_tensor(observations)

        prediction = self.model(x)

        value = float(
            prediction.detach().cpu().item()
        )

        return V4PredictionResult(
            predicted_future_degradation=value,
            model_name="EdgeResilience_V4_TemporalPredictor",
            model_source=str(self.checkpoint_path),
            feature_count=self.config.input_features,
            observation_steps=self.config.sequence_length,
        )
