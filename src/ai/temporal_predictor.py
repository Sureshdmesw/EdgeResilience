from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import torch
import torch.nn as nn


@dataclass
class TemporalModelConfig:
    input_features: int = 17
    sequence_length: int = 12
    d_model: int = 64
    nhead: int = 4
    num_layers: int = 2
    dim_feedforward: int = 128
    dropout: float = 0.10


class EdgeResilienceTemporalPredictor(nn.Module):
    """
    EdgeResilience-native temporal predictive model.

    Input:
        [batch, sequence_length, input_features]

    Output:
        predicted future resilience degradation
        [batch]
    """

    def __init__(
        self,
        config: TemporalModelConfig | None = None,
    ):
        super().__init__()

        self.config = (
            config
            if config is not None
            else TemporalModelConfig()
        )

        self.input_projection = nn.Linear(
            self.config.input_features,
            self.config.d_model,
        )

        self.position_embedding = nn.Parameter(
            torch.zeros(
                1,
                self.config.sequence_length,
                self.config.d_model,
            )
        )

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=self.config.d_model,
            nhead=self.config.nhead,
            dim_feedforward=self.config.dim_feedforward,
            dropout=self.config.dropout,
            batch_first=True,
            norm_first=True,
        )

        self.encoder = nn.TransformerEncoder(
            encoder_layer,
            num_layers=self.config.num_layers,
        )

        self.temporal_attention = nn.Linear(
            self.config.d_model,
            1,
        )

        self.output_head = nn.Sequential(
            nn.LayerNorm(self.config.d_model),
            nn.Linear(
                self.config.d_model,
                32,
            ),
            nn.GELU(),
            nn.Dropout(self.config.dropout),
            nn.Linear(32, 1),
            nn.Sigmoid(),
        )

    def forward(
        self,
        x: torch.Tensor,
    ) -> torch.Tensor:

        if x.ndim != 3:
            raise ValueError(
                "Expected input shape "
                "[batch, sequence, features]"
            )

        if x.shape[1] != self.config.sequence_length:
            raise ValueError(
                f"Expected sequence length "
                f"{self.config.sequence_length}, "
                f"got {x.shape[1]}"
            )

        if x.shape[2] != self.config.input_features:
            raise ValueError(
                f"Expected {self.config.input_features} "
                f"features, got {x.shape[2]}"
            )

        x = self.input_projection(x)

        x = x + self.position_embedding

        encoded = self.encoder(x)

        attention_scores = self.temporal_attention(
            encoded
        )

        attention_weights = torch.softmax(
            attention_scores,
            dim=1,
        )

        pooled = torch.sum(
            encoded * attention_weights,
            dim=1,
        )

        return self.output_head(
            pooled
        ).squeeze(-1)


def build_model() -> EdgeResilienceTemporalPredictor:
    return EdgeResilienceTemporalPredictor()


if __name__ == "__main__":

    model = build_model()

    x = torch.randn(
        4,
        12,
        17,
    )

    with torch.no_grad():
        y = model(x)

    print("=" * 80)
    print("EDGERESILIENCE TEMPORAL MODEL")
    print("=" * 80)
    print(f"Input: {tuple(x.shape)}")
    print(f"Output: {tuple(y.shape)}")
    print(
        f"Parameters: "
        f"{sum(p.numel() for p in model.parameters()):,}"
    )
    print()
    print("TEMPORAL_MODEL = PASS")
