import json
from pathlib import Path

p = Path(r"experiments\v4_fp32_boundary_probe_result.json")

data = {
    "compile_job": "jp4yzxx8p",
    "target_model": "mq26o5ojn",
    "inference_job": "jpvlj1er5",
    "input_shape": [1, 12, 17],
    "input_dtype": "float32",
    "final_output": 0.01112366,
    "reduce_sum_output_first16": [
        1.1591798, 2.5195315, -1.3779298, -3.4882815,
        1.0947267, -0.03533936, 2.6269534, 0.27734378,
        0.4829102, -0.48461917, 1.2041017, 0.05535889,
        0.93994147, -0.3964844, -0.05514527, 0.6469727
    ],
    "production_baseline": 0.011123658157885075,
    "conclusion": "Exposing the ReduceSum transformer boundary does not alter the production Snapdragon final output."
}

p.write_text(json.dumps(data, indent=2))
print(p)
