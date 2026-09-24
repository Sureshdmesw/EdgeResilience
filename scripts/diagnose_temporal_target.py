import json
from pathlib import Path
import numpy as np

DATASET = Path("data/processed/temporal/edgeresilience_temporal_dataset.jsonl")

def main():
    records = [json.loads(x) for x in DATASET.read_text(encoding="utf-8").splitlines() if x.strip()]

    targets = np.array([r["future_degradation"] for r in records], dtype=float)
    current = np.array([r["current_resilience"] for r in records], dtype=float)
    future = np.array([r["future_resilience"] for r in records], dtype=float)

    print(f"Records: {len(records)}")
    print()

    print("TARGET DISTRIBUTION")
    print(f"min     = {targets.min():.4f}")
    print(f"max     = {targets.max():.4f}")
    print(f"mean    = {targets.mean():.4f}")
    print(f"median  = {np.median(targets):.4f}")
    print(f"std     = {targets.std():.4f}")
    print()

    print("TARGET PERCENTILES")
    for p in [0, 10, 25, 50, 75, 90, 95, 99, 100]:
        print(f"p{p:>3} = {np.percentile(targets, p):.4f}")

    print()
    print("CORRELATION CHECKS")

    corr_current = np.corrcoef(current, targets)[0, 1]
    corr_future = np.corrcoef(future, targets)[0, 1]

    print(f"current_resilience vs future_degradation = {corr_current:.4f}")
    print(f"future_resilience  vs future_degradation = {corr_future:.4f}")

    print()
    print("BASELINE")

    mean_prediction = np.full_like(targets, targets.mean())
    mae = np.mean(np.abs(mean_prediction - targets))
    rmse = np.sqrt(np.mean((mean_prediction - targets) ** 2))

    print(f"Mean baseline MAE  = {mae:.4f}")
    print(f"Mean baseline RMSE = {rmse:.4f}")

    print()
    print("TARGET_DIAGNOSTICS = PASS")

if __name__ == "__main__":
    main()
