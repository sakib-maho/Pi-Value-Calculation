"""Monte Carlo estimation utilities for pi."""

from __future__ import annotations

import csv
import math
import random
from pathlib import Path
from statistics import pstdev


HistoryRow = tuple[int, float, float]


def _validate_samples(samples: int) -> None:
    if samples <= 0:
        raise ValueError("samples must be greater than zero")


def _normalize_checkpoints(samples: int, checkpoints: list[int] | tuple[int, ...] | None) -> list[int]:
    if not checkpoints:
        return []

    normalized: set[int] = set()
    for checkpoint in checkpoints:
        if checkpoint <= 0:
            raise ValueError("checkpoints must be greater than zero")
        normalized.add(min(checkpoint, samples))

    return sorted(normalized)


def estimate_pi(samples: int, seed: int = 7) -> float:
    """Estimate pi by sampling random points in the unit square."""
    estimate, _ = estimate_pi_with_history(samples=samples, seed=seed, checkpoints=[samples])
    return estimate


def estimate_pi_with_history(
    samples: int,
    seed: int = 7,
    checkpoints: list[int] | tuple[int, ...] | None = None,
) -> tuple[float, list[HistoryRow]]:
    """Estimate pi and return progress snapshots at requested checkpoints."""
    _validate_samples(samples)
    checkpoint_values = _normalize_checkpoints(samples, checkpoints)
    rng = random.Random(seed)
    inside = 0
    history: list[HistoryRow] = []

    checkpoints_set = set(checkpoint_values)
    for index in range(1, samples + 1):
        x = rng.uniform(-1, 1)
        y = rng.uniform(-1, 1)
        if x * x + y * y <= 1:
            inside += 1

        if index in checkpoints_set:
            estimate = 4 * inside / index
            history.append((index, estimate, abs(estimate - math.pi)))

    final_estimate = 4 * inside / samples
    return final_estimate, history


def multi_seed_stats(samples: int, seeds: list[int] | tuple[int, ...]) -> dict[str, float | list[float] | int]:
    """Run the estimator across multiple seeds and summarize the estimates."""
    _validate_samples(samples)
    if not seeds:
        raise ValueError("at least one seed is required")

    estimates = [estimate_pi(samples=samples, seed=seed) for seed in seeds]
    mean = sum(estimates) / len(estimates)
    std_dev = pstdev(estimates) if len(estimates) > 1 else 0.0
    return {
        "samples": samples,
        "seed_count": len(seeds),
        "mean": mean,
        "std_dev": std_dev,
        "min": min(estimates),
        "max": max(estimates),
        "estimates": estimates,
    }


def export_history_to_csv(history: list[HistoryRow], destination: str | Path) -> Path:
    """Persist estimation history to a CSV file."""
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["samples", "estimate_pi", "abs_error_vs_math_pi"])
        for row in history:
            writer.writerow(row)
    return path
