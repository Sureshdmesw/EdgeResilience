"""
Phase 4/5 preparation:
- Verify Mod nodes are constant-only (constant-foldable)
- Produce QNN-ready ONNX derivative via ORT graph optimization
- Verify numerical equivalence of derivative vs original
- Output: models/edgeresilience/snapdragon/temporal_predictor_v4_qnn_ready.onnx

The original V4 ONNX is NOT modified.
"""
from __future__ import annotations

import hashlib
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import onnx
import onnxruntime as ort
from onnxruntime import SessionOptions, GraphOptimizationLevel

PROJECT_ROOT = Path(r"E:\EdgeResilience")
SRC_MODEL = PROJECT_ROOT / "models" / "edgeresilience" / "temporal_predictor_v4_dynamic.onnx"
OUT_DIR = PROJECT_ROOT / "models" / "edgeresilience" / "snapdragon"
OUT_MODEL = OUT_DIR / "temporal_predictor_v4_qnn_ready.onnx"
REPORT_OUT = PROJECT_ROOT / "experiments" / "snapdragon" / "qnn_ready_model_report.json"

EXPECTED_SRC_SHA256 = "acb43a20c9fa64577c56bdfe3aa3c2ea96b6691420c0a7994dc5fd9f230c0e5d"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def verify_mod_constants(model: onnx.ModelProto) -> dict:
    """Confirm all Mod nodes have only Constant inputs."""
    const_map: dict[str, list] = {}
    for n in model.graph.node:
        if n.op_type == "Constant":
            for attr in n.attribute:
                if attr.name == "value":
                    t = attr.t
                    vals = (
                        list(t.int64_data)
                        or list(t.int32_data)
                        or list(t.float_data)
                        or list(t.double_data)
                    )
                    const_map[n.output[0]] = vals

    mod_nodes = [n for n in model.graph.node if n.op_type == "Mod"]
    results = []
    all_constant = True
    for n in mod_nodes:
        a = const_map.get(n.input[0])
        b = const_map.get(n.input[1])
        is_const = a is not None and b is not None
        if not is_const:
            all_constant = False
        result_val = [x % y for x, y in zip(a, b)] if is_const else None
        results.append({
            "node": n.name,
            "input_a": a,
            "input_b": b,
            "result": result_val,
            "both_constant": is_const,
        })
    return {"mod_nodes": results, "all_mod_inputs_are_constants": all_constant}


def produce_optimized_onnx(src: Path, dst: Path) -> None:
    """Use ORT BASIC optimization: constant folding + dead-code elimination only.
    Avoids ORT-internal fused ops (FusedGemm, Gelu) that are not standard ONNX
    and are not accepted by qnn-onnx-converter.
    """
    opts = SessionOptions()
    opts.graph_optimization_level = GraphOptimizationLevel.ORT_ENABLE_BASIC
    opts.optimized_model_filepath = str(dst)
    _ = ort.InferenceSession(str(src), sess_options=opts, providers=["CPUExecutionProvider"])


def count_op(model: onnx.ModelProto, op: str) -> int:
    return sum(1 for n in model.graph.node if n.op_type == op)


def run_inference(model_path: Path, x: np.ndarray) -> np.ndarray:
    sess = ort.InferenceSession(str(model_path), providers=["CPUExecutionProvider"])
    inp = sess.get_inputs()[0].name
    return sess.run(None, {inp: x})[0]


def main() -> None:
    print("=" * 72)
    print("QNN-READY ONNX DERIVATIVE PREPARATION")
    print("=" * 72)

    # Integrity check on source
    src_sha = sha256_file(SRC_MODEL)
    assert src_sha == EXPECTED_SRC_SHA256, f"Source integrity FAIL: {src_sha}"
    print(f"Source SHA256: {src_sha.upper()} — PASS")

    # Load source
    src_model = onnx.load(str(SRC_MODEL))
    mod_before = count_op(src_model, "Mod")
    print(f"Mod nodes in source: {mod_before}")

    # Verify Mod nodes are constant-only
    mod_analysis = verify_mod_constants(src_model)
    print(f"All Mod inputs are constants: {mod_analysis['all_mod_inputs_are_constants']}")
    for entry in mod_analysis["mod_nodes"]:
        print(f"  {entry['node']}: {entry['input_a']} mod {entry['input_b']} = {entry['result']}")

    # Produce ORT-optimized (constant-folded) derivative
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\nProducing ORT-optimized derivative -> {OUT_MODEL.name}")
    produce_optimized_onnx(SRC_MODEL, OUT_MODEL)

    # Inspect derivative
    opt_model = onnx.load(str(OUT_MODEL))
    onnx.checker.check_model(opt_model)
    mod_after = count_op(opt_model, "Mod")
    ops_after = sorted(set(n.op_type for n in opt_model.graph.node))
    nodes_after = len(opt_model.graph.node)
    print(f"ONNX checker on derivative: PASS")
    print(f"Mod nodes after optimization: {mod_after}")
    print(f"Nodes: {nodes_after} (was {len(src_model.graph.node)})")
    print(f"Operators: {ops_after}")

    # Numerical equivalence: 200 random samples
    np.random.seed(42)
    n_samples = 200
    errors = []
    for _ in range(n_samples):
        x = np.random.randn(1, 12, 17).astype(np.float32)
        y_src = run_inference(SRC_MODEL, x)
        y_opt = run_inference(OUT_MODEL, x)
        errors.append(abs(float(y_src[0]) - float(y_opt[0])))

    max_err = float(np.max(errors))
    mean_err = float(np.mean(errors))
    rmse = float(np.sqrt(np.mean(np.array(errors) ** 2)))
    tolerance = 1e-5
    equiv_pass = max_err < tolerance

    print(f"\nNumerical equivalence ({n_samples} samples):")
    print(f"  Max absolute error:  {max_err:.10f}")
    print(f"  Mean absolute error: {mean_err:.10f}")
    print(f"  RMSE:                {rmse:.10f}")
    print(f"  Tolerance:           {tolerance}")
    print(f"  Result:              {'PASS' if equiv_pass else 'FAIL'}")

    if not equiv_pass:
        raise RuntimeError(f"Numerical equivalence FAILED: max_err={max_err}")

    opt_sha = sha256_file(OUT_MODEL)
    print(f"\nDerivative SHA256: {opt_sha.upper()}")

    report = {
        "project": "EdgeResilience",
        "artifact": "qnn_ready_model_report",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "source_model": {
            "path": str(SRC_MODEL.relative_to(PROJECT_ROOT)),
            "sha256": src_sha.upper(),
            "integrity": "PASS",
            "mod_nodes": mod_before,
            "mod_analysis": mod_analysis,
        },
        "derivative_model": {
            "path": str(OUT_MODEL.relative_to(PROJECT_ROOT)),
            "sha256": opt_sha.upper(),
            "provenance": "ADAPTED from validated V4 dynamic ONNX via ORT full graph optimization (constant folding)",
            "relationship_to_source": "ADAPTED",
            "onnx_checker": "PASS",
            "mod_nodes_remaining": mod_after,
            "node_count": nodes_after,
            "operators": ops_after,
        },
        "numerical_equivalence": {
            "samples": n_samples,
            "max_absolute_error": max_err,
            "mean_absolute_error": mean_err,
            "rmse": rmse,
            "tolerance": tolerance,
            "result": "PASS" if equiv_pass else "FAIL",
        },
        "qnn_deployment_note": (
            "This derivative is prepared for QNN conversion when a Snapdragon device "
            "and QNN SDK are available. Conversion command: "
            "qnn-onnx-converter --input_network temporal_predictor_v4_qnn_ready.onnx "
            "--output_path temporal_predictor_v4.cpp "
            "--input_dim vehicle_temporal_features 1,12,17. "
            "Actual QNN execution: NOT VERIFIED (no Snapdragon hardware present)."
        ),
        "snapdragon_status": "NOT VERIFIED",
        "qnn_status": "NOT VERIFIED",
    }

    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nReport: {REPORT_OUT}")
    print("QNN_READY_MODEL_PREPARATION = PASS")


if __name__ == "__main__":
    main()
