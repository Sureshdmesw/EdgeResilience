import json
from pathlib import Path

base = Path(r"E:\EdgeResilience\artifacts\qaihub\jp3z9xmx5")
src = base / "jp3z9xmx5_1_0_qhas_summary.json"
out = base / "qhas_summary_extracted.json"

data = json.loads(src.read_text(encoding="utf-8"))

summary = data["data"]["htp_overall_summary"]["data"][0]

result = {
    "job_id": "jp3z9xmx5",
    "artifact": "QHAS",
    "htp": summary.get("htp"),
    "percent_idle": summary.get("percent_idle"),
    "percent_utilization": summary.get("percent_utilization"),
    "time_us": summary.get("time_us"),
    "graph_execute_us": summary.get("graph_execute_us"),
    "inferences_per_second": summary.get("inf_per_s"),
    "timeline_cycles": summary.get("timeline_cycles"),
    "total_dram_read_bytes": summary.get("total_dram_read"),
    "total_dram_write_bytes": summary.get("total_dram_write"),
    "total_dram_bytes": summary.get("total_dram"),
    "peak_vtcm_alloc_bytes": summary.get("peak_vtcm_alloc"),
    "total_vtcm_read_bytes": summary.get("total_vtcm_read"),
    "total_vtcm_write_bytes": summary.get("total_vtcm_write"),
    "total_vtcm_bytes": summary.get("total_vtcm"),
    "unique_qnn_ops": summary.get("unique_qnn_ops"),
    "qnn_nodes": summary.get("qnn_nodes"),
    "unique_htp_ops": summary.get("unique_htp_ops"),
    "htp_nodes": summary.get("htp_nodes"),
}

out.write_text(json.dumps(result, indent=2), encoding="utf-8")

print(json.dumps(result, indent=2))
print(f"\nSaved: {out}")
