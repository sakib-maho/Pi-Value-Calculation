# Monte Carlo Pi

`monte-carlo-pi` estimates `math.pi` by randomly throwing points into a square and
measuring how many fall inside the inscribed circle. It is a compact teaching repo
for probability, simulation, and CLI-friendly experimentation.

## How It Works

For each sample, the program picks an `(x, y)` point uniformly from `[-1, 1]`.
Points inside the unit circle satisfy `x^2 + y^2 <= 1`. The ratio of inside points
to all points approximates the circle-to-square area ratio:

`inside / total ~= pi / 4`

So the estimator is:

`pi ~= 4 * inside / total`

As the sample count increases, the estimate usually converges toward `math.pi`.

## Features

- Deterministic `estimate_pi(samples, seed)` helper
- History snapshots with absolute error tracking
- Multi-seed aggregate statistics for quick stability checks
- Optional CSV export for convergence analysis
- CLI that reports the error versus `math.pi`
- Thorough tests for library functions and command behavior

## CLI Examples

```bash
python3 cli.py --samples 100000 --seed 7
python3 cli.py --samples 50000 --seed 7 --history 100,1000,10000,50000
python3 cli.py --samples 50000 --history 100,1000,10000 --csv out/history.csv
python3 cli.py --samples 20000 --seeds 1,2,3,4,5
```

Example output:

```text
estimate=3.136400
error_vs_math_pi=0.005193
history[100]=3.080000 error=0.061593
history[1000]=3.180000 error=0.038407
```

## Python API

```python
from pi_calc.monte_carlo import (
    estimate_pi,
    estimate_pi_with_history,
    export_history_to_csv,
    multi_seed_stats,
)

estimate = estimate_pi(100_000, seed=42)
estimate, history = estimate_pi_with_history(50_000, seed=42, checkpoints=[100, 1000, 10_000])
stats = multi_seed_stats(20_000, seeds=[1, 2, 3, 4, 5])
export_history_to_csv(history, "history.csv")
```

## Run Tests

```bash
python3 -m pytest -q
```

## License

MIT. See `LICENSE`.
