from pathlib import Path
import hashlib
import json
import numpy as np

ROOT = Path(r"E:\EdgeResilience")

cpu_file = ROOT / "experiments" / "v4_output_head_control_input.npy"
snap_file = ROOT / "experiments" / "v4_reducesum_boundary_snapdragon_output.npy"

cpu = np.load(cpu_file).astype(np.float32)
snap = np.load(snap_file).astype(np.float32)

cpu = cpu.reshape(1, 64)
snap = snap.reshape(1, 64)

diff = snap - cpu
abs_diff = np.abs(diff)

max_idx = int(np.argmax(abs_diff))
max_error = float(abs_diff.reshape(-1)[max_idx])
mean_error = float(abs_diff.mean())
rmse = float(np.sqrt(np.mean(diff ** 2)))

relative = abs_diff / np.maximum(np.abs(cpu), 1e-12)

print("CPU SHAPE:", cpu.shape)
print("SNAPDRAGON SHAPE:", snap.shape)

print()
print("CPU FIRST 8:")
print(cpu[0, :8])

print()
print("SNAPDRAGON FIRST 8:")
print(snap[0, :8])

print()
print("=== BOUNDARY COMPARISON ===")
print("MAX ABS ERROR:", max_error)
print("MAX ERROR INDEX:", max_idx)
print("MEAN ABS ERROR:", mean_error)
print("RMSE:", rmse)
print("MAX RELATIVE ERROR:", float(relative.max()))
print("MEAN RELATIVE ERROR:", float(relative.mean()))

print()
print("CPU AT MAX ERROR:", float(cpu.reshape(-1)[max_idx]))
print("SNAP AT MAX ERROR:", float(snap.reshape(-1)[max_idx]))
print("SIGNED ERROR:", float(diff.reshape(-1)[max_idx]))

print()
print("CPU MIN:", float(cpu.min()))
print("CPU MAX:", float(cpu.max()))
print("CPU MEAN:", float(cpu.mean()))
print("CPU STD:", float(cpu.std()))

print()
print("SNAP MIN:", float(snap.min()))
print("SNAP MAX:", float(snap.max()))
print("SNAP MEAN:", float(snap.mean()))
print("SNAP STD:", float(snap.std()))

report = {
    "cpu_file": str(cpu_file),
    "snapdragon_file": str(snap_file),
    "max_abs_error": max_error,
    "max_error_index": max_idx,
    "mean_abs_error": mean_error,
    "rmse": rmse,
    "max_relative_error": float(relative.max()),
    "mean_relative_error": float(relative.mean()),
    "cpu_at_max_error": float(cpu.reshape(-1)[max_idx]),
    "snapdragon_at_max_error": float(snap.reshape(-1)[max_idx]),
    "signed_error_at_max": float(diff.reshape(-1)[max_idx])
}

report_file = ROOT / "experiments" / "v4_reducesum_boundary_comparison.json"
report_file.write_text(json.dumps(report, indent=2), encoding="utf-8")

print()
print("REPORT:", report_file)
