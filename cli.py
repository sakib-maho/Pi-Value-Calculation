"""CLI for estimating PI with Monte Carlo simulation."""

from __future__ import annotations

import argparse

from pi_calc.monte_carlo import estimate_pi


def main() -> int:
    parser = argparse.ArgumentParser(description="Estimate PI using Monte Carlo simulation.")
    parser.add_argument("--samples", type=int, default=10000)
    args = parser.parse_args()
    value = estimate_pi(args.samples)
    print(f"{value:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
