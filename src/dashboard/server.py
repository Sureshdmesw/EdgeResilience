# -*- coding: utf-8 -*-
"""
EdgeResilience — Edge AI Safety Intelligence Console
Competition-grade dashboard for Qualcomm Snapdragon AI Lab Build and Present Challenge.

Zero external dependencies. Python stdlib HTTP server only.
Run: python src/dashboard/server.py
Open: http://127.0.0.1:8765
"""
from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_FILE = PROJECT_ROOT / "data" / "evidence" / "v4_demo_scenario.json"
BENCHMARK_FILE = PROJECT_ROOT / "experiments" / "v4_pytorch_vs_onnx_cpu_benchmark.json"
ABLATION_FILE = PROJECT_ROOT / "experiments" / "v4_neural_ablation_report.json"
EQUIV_FILE = PROJECT_ROOT / "experiments" / "v4_dynamic_onnx_equivalence_report.json"
CPU_BENCH_FILE = PROJECT_ROOT / "experiments" / "cpu_reference_benchmark_v4.json"
MODEL_REPORT_FILE = PROJECT_ROOT / "models" / "edgeresilience" / "temporal_predictor_v4_report.json"
DEPLOY_MANIFEST_FILE = PROJECT_ROOT / "experiments" / "snapdragon_deployment_manifest_v4.json"

HOST = "127.0.0.1"
PORT = 8765

DASHBOARD_DIR = Path(__file__).resolve().parent


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"error": str(e), "path": str(path)}


def _build_html() -> str:
    parts = ["_part1_head.html", "_part2_body.html", "_part3_pages.html"]
    html = ""
    for part in parts:
        p = DASHBOARD_DIR / part
        if p.exists():
            html += p.read_text(encoding="utf-8")
        else:
            html += f"<!-- MISSING: {part} -->"
    return html


class DashboardHandler(BaseHTTPRequestHandler):

    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html: str) -> None:
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/api/evidence":
            if not EVIDENCE_FILE.exists():
                self._send_json({"error": "Evidence file not found. Run: python scripts/generate_v4_demo_evidence.py"}, 404)
                return
            self._send_json(_load_json(EVIDENCE_FILE))
            return

        if self.path == "/api/meta":
            meta = {
                "model_report": _load_json(MODEL_REPORT_FILE) if MODEL_REPORT_FILE.exists() else {},
                "benchmark": _load_json(BENCHMARK_FILE) if BENCHMARK_FILE.exists() else {},
                "ablation": _load_json(ABLATION_FILE) if ABLATION_FILE.exists() else {},
                "equivalence": _load_json(EQUIV_FILE) if EQUIV_FILE.exists() else {},
                "cpu_bench": _load_json(CPU_BENCH_FILE) if CPU_BENCH_FILE.exists() else {},
                "deploy_manifest": _load_json(DEPLOY_MANIFEST_FILE) if DEPLOY_MANIFEST_FILE.exists() else {},
            }
            self._send_json(meta)
            return

        self._send_html(DASHBOARD_HTML)

    def log_message(self, fmt: str, *args) -> None:
        print(f"[dashboard] {fmt % args}")


def main() -> None:
    global DASHBOARD_HTML
    DASHBOARD_HTML = _build_html()
    server = HTTPServer((HOST, PORT), DashboardHandler)
    print("=" * 72)
    print("EDGERESILIENCE — EDGE AI SAFETY INTELLIGENCE CONSOLE")
    print("=" * 72)
    print(f"Evidence : {EVIDENCE_FILE}")
    print(f"Dashboard: http://{HOST}:{PORT}")
    print(f"API      : http://{HOST}:{PORT}/api/evidence")
    print(f"Meta API : http://{HOST}:{PORT}/api/meta")
    print("Press Ctrl+C to stop.")
    print("=" * 72)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
    finally:
        server.server_close()


DASHBOARD_HTML = ""

if __name__ == "__main__":
    main()
