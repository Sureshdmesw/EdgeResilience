import hashlib
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


# ---------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------

SEED = 42

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

DATASET = (
    ROOT
    / "data"
    / "processed"
    / "temporal"
    / "edgeresilience_temporal_dataset_v4.jsonl"
)

MODEL_DIR = (
    ROOT
    / "models"
    / "edgeresilience"
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

CHECKPOINT = (
    MODEL_DIR
    / "temporal_predictor_v4.pt"
)

REPORT = (
    MODEL_DIR
    / "temporal_predictor_v4_report.json"
)


# ---------------------------------------------------------------------
# Load dataset
# ---------------------------------------------------------------------

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

X = np.asarray(
    [
        [
            [
                observation[name]
                for name in feature_names
            ]
            for observation in record["observations"]
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


# ---------------------------------------------------------------------
# Train/test split
# ---------------------------------------------------------------------

indices = np.arange(
    len(records)
)

train_idx, test_idx = train_test_split(
    indices,
    test_size=0.20,
    random_state=SEED,
)

# Validation split from training only
train_idx, val_idx = train_test_split(
    train_idx,
    test_size=0.20,
    random_state=SEED,
)


X_train = X[train_idx]
X_val = X[val_idx]
X_test = X[test_idx]

y_train = y[train_idx]
y_val = y[val_idx]
y_test = y[test_idx]


# ---------------------------------------------------------------------
# Training-only feature normalization
# ---------------------------------------------------------------------

mean = X_train.mean(
    axis=(0, 1),
    keepdims=True,
)

std = X_train.std(
    axis=(0, 1),
    keepdims=True,
)

std = np.maximum(
    std,
    1e-6,
)

X_train = (
    X_train - mean
) / std

X_val = (
    X_val - mean
) / std

X_test = (
    X_test - mean
) / std


# ---------------------------------------------------------------------
# Torch datasets
# ---------------------------------------------------------------------

train_dataset = TensorDataset(
    torch.from_numpy(X_train),
    torch.from_numpy(y_train),
)

val_dataset = TensorDataset(
    torch.from_numpy(X_val),
    torch.from_numpy(y_val),
)

train_loader = DataLoader(
    train_dataset,
    batch_size=128,
    shuffle=True,
)

val_loader = DataLoader(
    val_dataset,
    batch_size=256,
    shuffle=False,
)


# ---------------------------------------------------------------------
# Device
# ---------------------------------------------------------------------

device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


# ---------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------

config = TemporalModelConfig(
    input_features=len(feature_names),
    sequence_length=X.shape[1],
    d_model=64,
    nhead=4,
    num_layers=2,
    dim_feedforward=128,
    dropout=0.10,
)

model = EdgeResilienceTemporalPredictor(
    config
).to(device)


# ---------------------------------------------------------------------
# Training configuration
# ---------------------------------------------------------------------

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=1e-3,
    weight_decay=1e-4,
)

loss_fn = nn.MSELoss()

EPOCHS = 80
PATIENCE = 12

best_val_loss = float("inf")
best_epoch = 0
patience_counter = 0


# ---------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------

print("=" * 90)
print("EDGERESILIENCE V4 TEMPORAL MODEL TRAINING")
print("=" * 90)

print(f"Dataset: {DATASET}")
print(f"Samples: {len(records)}")
print(f"Train: {len(train_idx)}")
print(f"Validation: {len(val_idx)}")
print(f"Test: {len(test_idx)}")
print(f"Sequence: {X.shape[1]} x {X.shape[2]}")
print(f"Device: {device}")
print(
    f"Parameters: "
    f"{sum(p.numel() for p in model.parameters()):,}"
)
print()

for epoch in range(1, EPOCHS + 1):

    model.train()

    train_losses = []

    for xb, yb in train_loader:

        xb = xb.to(device)
        yb = yb.to(device)

        optimizer.zero_grad()

        pred = model(xb)

        loss = loss_fn(
            pred,
            yb,
        )

        loss.backward()

        torch.nn.utils.clip_grad_norm_(
            model.parameters(),
            max_norm=1.0,
        )

        optimizer.step()

        train_losses.append(
            loss.item()
        )

    model.eval()

    val_losses = []

    with torch.no_grad():

        for xb, yb in val_loader:

            xb = xb.to(device)
            yb = yb.to(device)

            pred = model(xb)

            loss = loss_fn(
                pred,
                yb,
            )

            val_losses.append(
                loss.item()
            )

    train_loss = float(
        np.mean(train_losses)
    )

    val_loss = float(
        np.mean(val_losses)
    )

    if (
        epoch == 1
        or epoch % 5 == 0
        or val_loss < best_val_loss
    ):
        print(
            f"Epoch {epoch:03d} | "
            f"train={train_loss:.6f} | "
            f"val={val_loss:.6f}"
        )

    if val_loss < best_val_loss:

        best_val_loss = val_loss
        best_epoch = epoch
        patience_counter = 0

        torch.save(
            {
                "model_state_dict": model.state_dict(),
                "config": config.__dict__,
                "feature_names": feature_names,
                "normalization_mean": mean.squeeze().tolist(),
                "normalization_std": std.squeeze().tolist(),
                "seed": SEED,
                "dataset": str(
                    DATASET.relative_to(ROOT)
                ),
                "model_type": (
                    "EdgeResilienceTemporalPredictor"
                ),
            },
            CHECKPOINT,
        )

    else:

        patience_counter += 1

        if patience_counter >= PATIENCE:

            print(
                f"Early stopping at epoch {epoch}"
            )

            break


# ---------------------------------------------------------------------
# Reload best checkpoint
# ---------------------------------------------------------------------

checkpoint = torch.load(
    CHECKPOINT,
    map_location=device,
)

model.load_state_dict(
    checkpoint["model_state_dict"]
)

model.eval()


# ---------------------------------------------------------------------
# Test inference
# ---------------------------------------------------------------------

X_test_tensor = torch.from_numpy(
    X_test
).to(device)

with torch.no_grad():

    predictions = (
        model(
            X_test_tensor
        )
        .cpu()
        .numpy()
    )

predictions = np.clip(
    predictions,
    0.0,
    1.0,
)

test_mae = mean_absolute_error(
    y_test,
    predictions,
)

test_rmse = mean_squared_error(
    y_test,
    predictions,
) ** 0.5


# ---------------------------------------------------------------------
# Mean baseline
# ---------------------------------------------------------------------

baseline = np.full_like(
    y_test,
    y_train.mean(),
)

baseline_mae = mean_absolute_error(
    y_test,
    baseline,
)

baseline_rmse = mean_squared_error(
    y_test,
    baseline,
) ** 0.5


# ---------------------------------------------------------------------
# Checkpoint checksum
# ---------------------------------------------------------------------

sha256 = hashlib.sha256()

with CHECKPOINT.open("rb") as f:

    for chunk in iter(
        lambda: f.read(1024 * 1024),
        b"",
    ):

        sha256.update(chunk)

checkpoint_sha256 = (
    sha256.hexdigest()
)


# ---------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------

report = {
    "artifact": (
        "EdgeResilience V4 temporal predictor"
    ),
    "dataset": str(
        DATASET.relative_to(ROOT)
    ),
    "dataset_records": len(records),
    "sequence_length": int(X.shape[1]),
    "features_per_step": int(X.shape[2]),
    "train_samples": int(len(train_idx)),
    "validation_samples": int(len(val_idx)),
    "test_samples": int(len(test_idx)),
    "seed": SEED,
    "device": str(device),
    "model_type": (
        "EdgeResilienceTemporalPredictor"
    ),
    "model_parameters": int(
        sum(
            p.numel()
            for p in model.parameters()
        )
    ),
    "config": config.__dict__,
    "optimizer": "AdamW",
    "learning_rate": 1e-3,
    "weight_decay": 1e-4,
    "batch_size": 128,
    "max_epochs": EPOCHS,
    "best_epoch": best_epoch,
    "best_validation_loss": best_val_loss,
    "test_mae": float(test_mae),
    "test_rmse": float(test_rmse),
    "mean_baseline_mae": float(
        baseline_mae
    ),
    "mean_baseline_rmse": float(
        baseline_rmse
    ),
    "beats_mean_baseline": bool(
        test_mae < baseline_mae
    ),
    "checkpoint": str(
        CHECKPOINT.relative_to(ROOT)
    ),
    "checkpoint_sha256": checkpoint_sha256,
    "snapdragon_hardware_verified": False,
    "physical_vehicle_test": False,
    "external_can_transmission": False,
    "direct_actuation": False,
    "provenance": (
        "new EdgeResilience artifact"
    ),
}

with REPORT.open(
    "w",
    encoding="utf-8",
) as f:

    json.dump(
        report,
        f,
        indent=2,
    )

print()
print("=" * 90)
print("EDGERESILIENCE V4 TRAINING RESULT")
print("=" * 90)

print(
    f"Best epoch: {best_epoch}"
)

print(
    f"Test MAE: {test_mae:.4f}"
)

print(
    f"Test RMSE: {test_rmse:.4f}"
)

print(
    f"Mean baseline MAE: "
    f"{baseline_mae:.4f}"
)

print(
    f"Mean baseline RMSE: "
    f"{baseline_rmse:.4f}"
)

print(
    f"Beats mean baseline: "
    f"{test_mae < baseline_mae}"
)

print(
    f"Checkpoint: {CHECKPOINT}"
)

print(
    f"SHA256: {checkpoint_sha256}"
)

print()
print("TEMPORAL_MODEL_TRAINING_V4 = PASS")
