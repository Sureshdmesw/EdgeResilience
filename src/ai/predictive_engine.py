from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Mapping, Sequence

import hashlib
import json

import numpy as np
import torch
import torch.nn as nn


# ============================================================
# EDGE RESILIENCE MODEL CONTRACT
# ============================================================

BINARY_FEATURES = [
    "authentication_failure_rate",
    "collision_event_flag",
    "connectivity_degradation_rate",
    "connectivity_drop_rate",
    "cyber_instability_index",
    "fire_explosion_flag",
    "message_integrity_failure_rate",
    "packet_loss_rate",
    "redundant_sensor_divergence",
    "replay_indicator_rate",
    "resilience_degradation_rate",
    "rolling_mean_3_message_integrity_failure_rate",
    "rolling_mean_3_packet_loss_rate",
    "rolling_mean_3_sensor_disagreement_rate",
    "rolling_std_3_message_integrity_failure_rate",
    "rolling_std_3_packet_loss_rate",
    "rolling_std_3_sensor_disagreement_rate",
    "rollover_flag",
    "safety_critical_ecu_ratio",
    "sensor_disagreement_rate",
    "sensor_plausibility_score",
    "sequence_counter_anomaly_rate",
    "speed_over_limit_flag",
    "state_transition_magnitude",
    "uds_request_rate",
    "unexpected_source_id_rate",
    "vehicle_damage_flag",
]

CONTINUOUS_FEATURES = [
    "VISION",
    "WEATHER",
    "can_bus_count",
    "can_bus_load_pct",
    "can_interarrival_jitter_ms",
    "can_interarrival_mean_ms",
    "can_message_rate",
    "can_message_rate_deviation",
    "d1_authentication_failure_rate",
    "d1_can_bus_load_pct",
    "d1_can_interarrival_jitter_ms",
    "d1_can_message_rate",
    "d1_connectivity_drop_rate",
    "d1_latency_jitter_ms",
    "d1_latency_ms",
    "d1_message_integrity_failure_rate",
    "d1_packet_loss_rate",
    "d1_replay_indicator_rate",
    "d1_sensor_disagreement_rate",
    "d1_sequence_counter_anomaly_rate",
    "d1_telemetry_gap_duration_ms",
    "diagnostic_event_rate",
    "ecu_count",
    "ecu_state_transition_rate",
    "latency_jitter_ms",
    "latency_ms",
    "rolling_mean_3_latency_ms",
    "rolling_std_3_latency_ms",
    "rssi_dbm",
    "speed_limit_deviation",
    "speed_limit_deviation_abs",
    "telemetry_gap_duration_ms",
]

FEATURES = BINARY_FEATURES + CONTINUOUS_FEATURES

FEATURE_COUNT = 59
OBSERVATION_STEPS = 12


# ============================================================
# MODEL
# ============================================================

class TemporalTransformer(nn.Module):
    """
    Architecture-compatible implementation of the inherited
    temporal Transformer.

    This class does not contain or embed a checkpoint.
    """

    def __init__(
        self,
        input_dim: int = FEATURE_COUNT,
        embedding_dim: int = 128,
        num_layers: int = 3,
        num_heads: int = 8,
        ff_dim: int = 256,
        dropout: float = 0.1,
        max_len: int = OBSERVATION_STEPS,
    ):
        super().__init__()

        self.input_projection = nn.Linear(
            input_dim,
            embedding_dim,
        )

        self.position = nn.Parameter(
            torch.zeros(
                1,
                max_len,
                embedding_dim,
            )
        )

        self.input_norm = nn.LayerNorm(
            embedding_dim
        )

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embedding_dim,
            nhead=num_heads,
            dim_feedforward=ff_dim,
            dropout=dropout,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )

        self.encoder = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_layers,
        )

        self.attention_pool = nn.Linear(
            embedding_dim,
            1,
        )

        self.pool_norm = nn.LayerNorm(
            embedding_dim
        )

        self.output_norm = nn.LayerNorm(
            embedding_dim
        )

        self.y3_head = nn.Linear(
            embedding_dim,
            1,
        )

        self.y6_head = nn.Linear(
            embedding_dim,
            1,
        )

    def forward(self, x: torch.Tensor):
        x = self.input_projection(x)
        x = self.input_norm(x)

        x = x + self.position[
            :,
            :x.size(1),
            :,
        ]

        x = self.encoder(x)

        scores = self.attention_pool(x)

        weights = torch.softmax(
            scores,
            dim=1,
        )

        pooled = torch.sum(
            weights * x,
            dim=1,
        )

        pooled = self.pool_norm(pooled)
        pooled = self.output_norm(pooled)

        y3 = self.y3_head(
            pooled
        ).squeeze(-1)

        y6 = self.y6_head(
            pooled
        ).squeeze(-1)

        return y3, y6


# ============================================================
# RESULT CONTRACT
# ============================================================

@dataclass(frozen=True)
class PredictionResult:
    y3_probability: float
    y6_probability: float
    y3_risk_level: str
    y6_risk_level: str
    model_name: str
    model_source: str
    feature_count: int
    observation_steps: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ============================================================
# HELPERS
# ============================================================

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def probability_to_level(
    probability: float,
) -> str:
    if probability < 0.05:
        return "NORMAL"

    if probability < 0.20:
        return "LOW"

    if probability < 0.50:
        return "MEDIUM"

    if probability < 0.80:
        return "HIGH"

    return "CRITICAL"


def safe_float(
    value: Any,
    default: float = 0.0,
) -> float:
    try:
        result = float(value)

        if not np.isfinite(result):
            return default

        return result

    except (TypeError, ValueError):
        return default


# ============================================================
# FEATURE MATRIX
# ============================================================

def build_feature_matrix(
    feature_records: Sequence[Mapping[str, Any]],
) -> np.ndarray:
    """
    Convert EdgeResilience feature records into the exact
    59-column model contract.

    Each record must contain feature names directly.
    Missing values are represented as zero.
    """

    rows: list[list[float]] = []

    for record in feature_records:
        row = [
            safe_float(
                record.get(
                    name,
                    0.0,
                )
            )
            for name in FEATURES
        ]

        rows.append(row)

    matrix = np.asarray(
        rows,
        dtype=np.float32,
    )

    matrix = np.nan_to_num(
        matrix,
        nan=0.0,
        posinf=0.0,
        neginf=0.0,
    )

    if matrix.ndim != 2:
        raise ValueError(
            f"Expected 2-D feature matrix, got {matrix.shape}."
        )

    if matrix.shape[1] != FEATURE_COUNT:
        raise ValueError(
            "Unexpected feature count: "
            f"{matrix.shape[1]}; expected {FEATURE_COUNT}."
        )

    for index in range(len(BINARY_FEATURES)):
        matrix[:, index] = np.clip(
            matrix[:, index],
            0.0,
            1.0,
        )

    return matrix


def build_window(
    feature_records: Sequence[Mapping[str, Any]],
) -> np.ndarray:
    """
    Build one 12-step model input window.
    """

    matrix = build_feature_matrix(
        feature_records
    )

    if matrix.shape[0] != OBSERVATION_STEPS:
        raise ValueError(
            "A prediction window requires exactly "
            f"{OBSERVATION_STEPS} timesteps; "
            f"received {matrix.shape[0]}."
        )

    return matrix.astype(
        np.float32,
        copy=False,
    )


# ============================================================
# MODEL LOADING
# ============================================================

def load_transformer_checkpoint(
    checkpoint_path: Path,
) -> TemporalTransformer:
    """
    Load a checkpoint into the architecture-compatible
    Transformer.

    This function does not modify the checkpoint.
    """

    model = TemporalTransformer()

    checkpoint = torch.load(
        checkpoint_path,
        map_location="cpu",
        weights_only=False,
    )

    if isinstance(checkpoint, dict):
        if "model_state_dict" in checkpoint:
            state_dict = checkpoint[
                "model_state_dict"
            ]
        elif "state_dict" in checkpoint:
            state_dict = checkpoint[
                "state_dict"
            ]
        else:
            state_dict = checkpoint
    else:
        state_dict = checkpoint

    model.load_state_dict(
        state_dict,
        strict=True,
    )

    model.eval()

    return model


# ============================================================
# PREDICTION
# ============================================================

def predict_window(
    model: TemporalTransformer,
    feature_records: Sequence[Mapping[str, Any]],
    *,
    model_name: str = "temporal_transformer",
    model_source: str = "edge_resilience",
) -> PredictionResult:
    """
    Run inference for one 12-step window.

    No vehicle actuation or control decision is performed here.
    """

    window = build_window(
        feature_records
    )

    tensor = torch.from_numpy(
        window
    ).unsqueeze(0)

    with torch.no_grad():
        y3_logits, y6_logits = model(
            tensor
        )

        y3_probability = float(
            torch.sigmoid(
                y3_logits
            )[0]
            .cpu()
            .item()
        )

        y6_probability = float(
            torch.sigmoid(
                y6_logits
            )[0]
            .cpu()
            .item()
        )

    return PredictionResult(
        y3_probability=y3_probability,
        y6_probability=y6_probability,
        y3_risk_level=probability_to_level(
            y3_probability
        ),
        y6_risk_level=probability_to_level(
            y6_probability
        ),
        model_name=model_name,
        model_source=model_source,
        feature_count=FEATURE_COUNT,
        observation_steps=OBSERVATION_STEPS,
    )


def save_prediction(
    result: PredictionResult,
    output_path: Path,
) -> None:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as handle:
        json.dump(
            result.to_dict(),
            handle,
            indent=2,
        )
        handle.write("\n")
