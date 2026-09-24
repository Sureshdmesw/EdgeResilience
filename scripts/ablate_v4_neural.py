import json
import random
from pathlib import Path
import sys

import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.ai.temporal_predictor import (
    EdgeResilienceTemporalPredictor,
    TemporalModelConfig,
)

SEED = 42

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

DATASET = (
    ROOT
    / "data"
    / "processed"
    / "temporal"
    / "edgeresilience_temporal_dataset_v4.jsonl"
)

records = [
    json.loads(line)
    for line in DATASET.open(
        "r",
        encoding="utf-8",
    )
]

feature_names = list(
    records[0]["observations"][0].keys()
)

X_seq = np.asarray(
    [
        [
            [obs[name] for name in feature_names]
            for obs in record["observations"]
        ]
        for record in records
    ],
    dtype=np.float32,
)

y = np.asarray(
    [
        record["future_degradation"]
        for record in records
    ],
    dtype=np.float32,
)

indices = np.arange(len(records))

train_idx, test_idx = train_test_split(
    indices,
    test_size=0.20,
    random_state=SEED,
)

train_idx, val_idx = train_test_split(
    train_idx,
    test_size=0.20,
    random_state=SEED,
)


def normalize_train_test(
    X_train,
    X_val,
    X_test,
):
    mean = X_train.mean(
        axis=tuple(range(X_train.ndim - 1)),
        keepdims=True,
    )

    std = X_train.std(
        axis=tuple(range(X_train.ndim - 1)),
        keepdims=True,
    )

    std = np.maximum(
        std,
        1e-6,
    )

    return (
        (X_train - mean) / std,
        (X_val - mean) / std,
        (X_test - mean) / std,
    )


def train_model(
    name,
    X_train,
    X_val,
    X_test,
):
    device = torch.device("cpu")

    config = TemporalModelConfig(
        input_features=X_train.shape[-1],
        sequence_length=X_train.shape[1],
        d_model=64,
        nhead=4,
        num_layers=2,
        dim_feedforward=128,
        dropout=0.10,
    )

    model = EdgeResilienceTemporalPredictor(
        config
    ).to(device)

    train_ds = TensorDataset(
        torch.from_numpy(X_train),
        torch.from_numpy(y[train_idx]),
    )

    val_ds = TensorDataset(
        torch.from_numpy(X_val),
        torch.from_numpy(y[val_idx]),
    )

    train_loader = DataLoader(
        train_ds,
        batch_size=128,
        shuffle=True,
    )

    val_loader = DataLoader(
        val_ds,
        batch_size=256,
        shuffle=False,
    )

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=1e-3,
        weight_decay=1e-4,
    )

    loss_fn = nn.MSELoss()

    best_state = None
    best_val = float("inf")
    patience = 0

    for epoch in range(1, 61):

        model.train()

        for xb, yb in train_loader:

            optimizer.zero_grad()

            pred = model(xb)

            loss = loss_fn(
                pred,
                yb,
            )

            loss.backward()

            torch.nn.utils.clip_grad_norm_(
                model.parameters(),
                1.0,
            )

            optimizer.step()

        model.eval()

        losses = []

        with torch.no_grad():

            for xb, yb in val_loader:

                pred = model(xb)

                losses.append(
                    loss_fn(
                        pred,
                        yb,
                    ).item()
                )

        val_loss = float(
            np.mean(losses)
        )

        if val_loss < best_val:

            best_val = val_loss

            best_state = {
                k: v.detach().clone()
                for k, v in model.state_dict().items()
            }

            patience = 0

        else:

            patience += 1

            if patience >= 10:
                break

    model.load_state_dict(
        best_state
    )

    model.eval()

    with torch.no_grad():

        pred = (
            model(
                torch.from_numpy(X_test)
            )
            .numpy()
        )

    pred = np.clip(
        pred,
        0.0,
        1.0,
    )

    mae = mean_absolute_error(
        y[test_idx],
        pred,
    )

    rmse = mean_squared_error(
        y[test_idx],
        pred,
    ) ** 0.5

    print(
        f"{name:<32}"
        f"MAE={mae:.4f} "
        f"RMSE={rmse:.4f}"
    )

    return mae, rmse


print("=" * 90)
print("EDGERESILIENCE V4 NEURAL ABLATION")
print("=" * 90)

# ------------------------------------------------------------
# A. Final timestep
# ------------------------------------------------------------

X_final = X_seq[:, -1:, :]

A_train, A_val, A_test = normalize_train_test(
    X_final[train_idx],
    X_final[val_idx],
    X_final[test_idx],
)

train_model(
    "FINAL TIMESTEP NEURAL",
    A_train,
    A_val,
    A_test,
)

# ------------------------------------------------------------
# B. Compact trajectory representation
# final + delta + temporal std
# ------------------------------------------------------------

final = X_seq[:, -1, :]
delta = X_seq[:, -1, :] - X_seq[:, 0, :]
std = X_seq.std(axis=1)

X_summary = np.stack(
    [
        final,
        delta,
        std,
    ],
    axis=1,
)

B_train, B_val, B_test = normalize_train_test(
    X_summary[train_idx],
    X_summary[val_idx],
    X_summary[test_idx],
)

train_model(
    "FINAL + DELTA + STD",
    B_train,
    B_val,
    B_test,
)

# ------------------------------------------------------------
# C. Full temporal sequence
# ------------------------------------------------------------

C_train, C_val, C_test = normalize_train_test(
    X_seq[train_idx],
    X_seq[val_idx],
    X_seq[test_idx],
)

train_model(
    "FULL 12-STEP NEURAL",
    C_train,
    C_val,
    C_test,
)

print()
print("NEURAL_ABLATION_V4 = PASS")
