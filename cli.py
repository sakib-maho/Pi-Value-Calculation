"""CLI for estimating pi with Monte Carlo simulation."""

from __future__ import annotations

import argparse
import math

from pi_calc.monte_carlo import (
    estimate_pi,
    estimate_pi_with_history,
    export_history_to_csv,
    multi_seed_stats,
)


def _parse_csv_ints(value: str) -> list[int]:
    return [int(part.strip()) for part in value.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Estimate pi using Monte Carlo simulation.")
    parser.add_argument("--samples", type=int, default=10_000, help="Number of random samples.")
    parser.add_argument("--seed", type=int, default=7, help="Seed for deterministic output.")
    parser.add_argument(
        "--history",
        type=_parse_csv_ints,
        help="Comma-separated checkpoints, such as 100,1000,10000.",
    )
    parser.add_argument(
        "--seeds",
        type=_parse_csv_ints,
        help="Run multiple seeds and report aggregate stats, for example 1,2,3.",
    )
    parser.add_argument("--csv", help="Write history checkpoints to a CSV file.")
    args = parser.parse_args()

    if args.seeds:
        stats = multi_seed_stats(samples=args.samples, seeds=args.seeds)
        print(f"mean={stats['mean']:.6f}")
        print(f"std_dev={stats['std_dev']:.6f}")
        print(f"min={stats['min']:.6f}")
        print(f"max={stats['max']:.6f}")
        print(f"error_vs_math_pi={abs(stats['mean'] - math.pi):.6f}")
        return 0

    history = args.history or []
    if history:
        value, snapshots = estimate_pi_with_history(args.samples, seed=args.seed, checkpoints=history)
        print(f"estimate={value:.6f}")
        print(f"error_vs_math_pi={abs(value - math.pi):.6f}")
        for sample_count, estimate, error in snapshots:
            print(f"history[{sample_count}]={estimate:.6f} error={error:.6f}")
        if args.csv:
            export_history_to_csv(snapshots, args.csv)
            print(f"history_csv={args.csv}")
        return 0

    value = estimate_pi(args.samples, seed=args.seed)
    print(f"estimate={value:.6f}")
    print(f"error_vs_math_pi={abs(value - math.pi):.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
