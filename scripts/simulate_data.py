import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.simulation import run_simulation


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run recommendation simulation and persist metrics."
    )
    parser.add_argument("--runs", type=int, default=250)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--output",
        type=str,
        default="docs/simulation_result.json",
        help="Output json path",
    )
    args = parser.parse_args()

    result = run_simulation(runs=args.runs, top_k=args.top_k, seed=args.seed)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    metrics = result["metrics"]
    print("Simulation finished")
    print(
        f"precision_at_k={metrics['precision_at_k']} | "
        f"baseline_precision_at_k={metrics['baseline_precision_at_k']} | "
        f"uplift_vs_baseline={metrics['uplift_vs_baseline']} | "
        f"viable_rate={metrics['viable_recommendation_rate']} | "
        f"avg_eta_min={metrics['avg_eta_min']} | "
        f"avg_delivery_fee_brl={metrics['avg_delivery_fee_brl']}"
    )
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()
