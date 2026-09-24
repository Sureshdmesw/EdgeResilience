import json
from pathlib import Path

base = Path(r"E:\EdgeResilience\artifacts\qaihub\jp3z9xmx5")
src = base / "jp3z9xmx5_1_0_qhas_summary.json"
out = base / "qhas_qnn_operator_summary.json"

data = json.loads(src.read_text(encoding="utf-8"))

ops = data["data"]["qnn_op_types"]["data"]

rows = []

for op in ops:
    rows.append({
        "op": op.get("op"),
        "cycles": op.get("cycles"),
        "percent_active_cycles": op.get("percent_active_cycles"),
        "dominant_path_percent": op.get("percent_dominant_path_cycles_htp_0"),
        "num_htp_ops": op.get("num_htp_ops"),
        "dram_read": op.get("dram_read"),
        "dram_write": op.get("dram_write"),
        "vtcm_read": op.get("vtcm_read"),
        "vtcm_write": op.get("vtcm_write")
    })

rows.sort(key=lambda x: x["cycles"] or 0, reverse=True)

out.write_text(json.dumps(rows, indent=2), encoding="utf-8")

print("Top QNN operations by HTP cycles:\n")

for i, row in enumerate(rows[:10], 1):
    print(
        f"{i:02d}. {row['op']:<25} "
        f"{row['cycles']:>6} cycles | "
        f"{row['percent_active_cycles']:.2f}% active"
    )

print(f"\nSaved: {out}")
