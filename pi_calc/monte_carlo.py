"""Monte Carlo estimation utilities for PI."""

from __future__ import annotations

import random


def estimate_pi(samples: int, seed: int = 7) -> float:
    rng = random.Random(seed)
    inside = 0
    for _ in range(samples):
        x = rng.uniform(-1, 1)
        y = rng.uniform(-1, 1)
        if x * x + y * y <= 1:
            inside += 1
    return 4 * inside / samples if samples > 0 else 0.0
